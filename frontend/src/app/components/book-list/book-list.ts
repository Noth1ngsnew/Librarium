import { Component, inject, signal, OnInit, computed } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { BookService } from '../../services/book.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-book-list',
  imports: [CommonModule],
  templateUrl: './book-list.html',
  styleUrl: './book-list.css'
})
export class BookList implements OnInit {
  private bookService = inject(BookService);
  private authService = inject(AuthService);
  private router = inject(Router);

  books = signal<any[]>([]);
  addedBookIds = signal<Set<number>>(new Set());
  loading = signal(true);
  error = signal('');
  coverUrls = signal<{ [key: number]: string }>({});
  selectedGenre = signal('All');

  genres = computed(() => {
    const all = this.books().map((b: any) => b.genre).filter(Boolean);
    return ['All', ...Array.from(new Set(all))];
  });

  filteredBooks = computed(() => {
    if (this.selectedGenre() === 'All') return this.books();
    return this.books().filter((b: any) => b.genre === this.selectedGenre());
  });

  ngOnInit() {
    this.loadAllBooks();
    this.loadMyBooks();
  }

  loadAllBooks() {
    this.bookService.getAllBooks().subscribe({
      next: (res: any) => {
        this.books.set(res);
        this.loading.set(false);
        this.loadCovers(res);
      },
      error: () => {
        this.error.set('Failed to load books.');
        this.loading.set(false);
      }
    });
  }

  loadMyBooks() {
    this.bookService.getMyBooks().subscribe({
      next: (res: any) => {
        const ids = new Set<number>(res.map((ub: any) => ub.book.id));
        this.addedBookIds.set(ids);
      }
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

  addToMyList(book: any) {
    this.bookService.addToMyList(book.id).subscribe({
      next: () => {
        const ids = new Set(this.addedBookIds());
        ids.add(book.id);
        this.addedBookIds.set(ids);
      },
      error: () => this.error.set('Failed to add book.')
    });
  }

  isAdded(bookId: number): boolean {
    return this.addedBookIds().has(bookId);
  }

  goToMyList() { this.router.navigate(['/my-list']); }
  goToBadges() { this.router.navigate(['/badges']); }
  goToProfile() { this.router.navigate(['/profile']); }

  logout() {
    this.authService.logout().subscribe({
      next: () => {
        this.authService.clearTokens();
        this.router.navigate(['/login']);
      }
    });
  }
}