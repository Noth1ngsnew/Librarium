import { Component, inject, signal, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule, TitleCasePipe } from '@angular/common';
import { BookService } from '../../services/book.service';

@Component({
  selector: 'app-my-list',
  imports: [CommonModule, TitleCasePipe],
  templateUrl: './my-list.html',
  styleUrl: './my-list.css'
})
export class MyList implements OnInit {
  private bookService = inject(BookService);
  private router = inject(Router);

  userBooks = signal<any[]>([]);
  filteredBooks = signal<any[]>([]);
  selectedStatus = signal('all');
  coverUrls = signal<{ [key: number]: string }>({});

  ngOnInit() {
    this.loadBooks();
  }

  loadBooks() {
    this.bookService.getMyBooks().subscribe({
      next: (res: any) => {
        this.userBooks.set(res);
        this.filterBooks();
        this.loadCovers(res.map((ub: any) => ub.book));
      },
      error: () => this.router.navigate(['/login'])
    });
  }

  loadCovers(books: any[]) {
    const cached: { [key: number]: string } = JSON.parse(localStorage.getItem('coverUrls') || '{}');
    const uncached = books.filter(book => !cached[book.id]);

    if (uncached.length === 0) {
      this.coverUrls.set(cached);
      return;
    }

    const promises = uncached.map(book => {
      const q = encodeURIComponent(`${book.title}+inauthor:${book.author}`);
      return fetch(`https://www.googleapis.com/books/v1/volumes?q=${q}&maxResults=1`)
        .then(r => r.json())
        .then(data => {
          const cover = data.items?.[0]?.volumeInfo?.imageLinks?.thumbnail;
          return { id: book.id, cover: cover ? cover.replace('http:', 'https:') : null };
        });
    });

    Promise.all(promises).then(results => {
      results.forEach(r => { if (r.cover) cached[r.id] = r.cover; });
      localStorage.setItem('coverUrls', JSON.stringify(cached));
      this.coverUrls.set({ ...cached });
    });
  }

  getCoverUrl(book: any): string {
    return this.coverUrls()[book.id] || `https://covers.openlibrary.org/b/title/${encodeURIComponent(book.title)}-M.jpg`;
  }

  filterBooks() {
    if (this.selectedStatus() === 'all') {
      this.filteredBooks.set(this.userBooks());
    } else {
      this.filteredBooks.set(
        this.userBooks().filter((ub: any) => ub.status === this.selectedStatus())
      );
    }
  }

  setStatus(status: string) {
    this.selectedStatus.set(status);
    this.filterBooks();
  }

  getCount(status: string): number {
    return this.userBooks().filter((ub: any) => ub.status === status).length;
  }

  goToDetail(id: number) {
    this.router.navigate(['/books', id]);
  }

  goBack() {
    this.router.navigate(['/books']);
  }

  getProgress(userBook: any): number {
    if (!userBook.book?.total_pages) return 0;
    return Math.round((userBook.current_page / userBook.book.total_pages) * 100);
  }
}