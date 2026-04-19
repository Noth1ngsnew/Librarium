import { Component, inject, signal, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BookService } from '../../services/book.service';

@Component({
  selector: 'app-book-detail',
  imports: [CommonModule, FormsModule],
  templateUrl: './book-detail.html',
  styleUrl: './book-detail.css'
})
export class BookDetail implements OnInit {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private bookService = inject(BookService);

  userBook = signal<any>(null);
  reviews = signal<any[]>([]);
  error = signal('');
  showCelebration = signal(false);
  coverUrl = signal('');

  newReview = { book: 0, content: '', rating: 5 };

  ngOnInit() {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.loadUserBook(id);
  }

  loadUserBook(id: number) {
    this.bookService.getUserBook(id).subscribe({
      next: (res: any) => {
        this.userBook.set(res);
        this.newReview.book = res.book.id;
        this.loadReviews(res.book.id);
        this.loadCover(res.book);
      },
      error: () => this.router.navigate(['/my-list'])
    });
  }

  loadCover(book: any) {
    const cached: { [key: number]: string } = JSON.parse(localStorage.getItem('coverUrls') || '{}');

    if (cached[book.id]) {
      this.coverUrl.set(cached[book.id]);
      return;
    }

    const q = encodeURIComponent(`${book.title}+inauthor:${book.author}`);
    fetch(`https://www.googleapis.com/books/v1/volumes?q=${q}&maxResults=1`)
      .then(r => r.json())
      .then(data => {
        const cover = data.items?.[0]?.volumeInfo?.imageLinks?.thumbnail;
        const url = cover
          ? cover.replace('http:', 'https:')
          : `https://covers.openlibrary.org/b/title/${encodeURIComponent(book.title)}-M.jpg`;

        cached[book.id] = url;
        localStorage.setItem('coverUrls', JSON.stringify(cached));
        this.coverUrl.set(url);
      });
  }

  loadReviews(bookId: number) {
    this.bookService.getBookReviews(bookId).subscribe({
      next: (res: any) => this.reviews.set(res)
    });
  }

  updateStatus(status: string) {
    this.bookService.patchUserBook(this.userBook().id, { status }).subscribe({
      next: (res: any) => this.userBook.set(res)
    });
  }

  updateCurrentPage(value: number) {
    const total = this.userBook()?.book?.total_pages ?? 0;
    const clamped = Math.min(Math.max(value, 0), total);
    this.userBook.update((ub: any) => ({ ...ub, current_page: clamped }));
  }

  updateProgress() {
    const total = this.userBook()?.book?.total_pages ?? 0;
    const current = this.userBook().current_page;
    const status = total > 0 && current >= total ? 'finished' : 'reading';

    this.bookService.patchUserBook(this.userBook().id, {
      current_page: current,
      status
    }).subscribe({
      next: (res: any) => {
        this.userBook.set(res);
        if (status === 'finished') this.celebrate();
      }
    });
  }

  celebrate() {
    this.showCelebration.set(true);
    setTimeout(() => this.showCelebration.set(false), 3000);
  }

  submitReview() {
    this.bookService.createReview(this.newReview).subscribe({
      next: () => {
        this.loadReviews(this.userBook().book.id);
        this.newReview.content = '';
        this.newReview.rating = 5;
      },
      error: () => this.error.set('Failed to submit review.')
    });
  }

  getProgress(): number {
    if (!this.userBook()?.book?.total_pages) return 0;
    return Math.round((this.userBook().current_page / this.userBook().book.total_pages) * 100);
  }

  getStars(rating: number): number[] {
    return Array(rating).fill(0);
  }

  getEmptyStars(rating: number): number[] {
    return Array(5 - rating).fill(0);
  }

  getCoverUrl(): string {
    return this.coverUrl() || `https://covers.openlibrary.org/b/title/${encodeURIComponent(this.userBook()?.book?.title)}-M.jpg`;
  }

  deleteFromMyList() {
    this.bookService.deleteUserBook(this.userBook().id).subscribe({
      next: () => this.router.navigate(['/my-list'])
    });
  }

  goBack() {
    this.router.navigate(['/my-list']);
  }
}