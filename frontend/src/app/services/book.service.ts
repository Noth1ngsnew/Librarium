import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class BookService {
  private http = inject(HttpClient);
  private apiUrl = 'http://localhost:8000/api';

  // Каталог
  getAllBooks() {
    return this.http.get(`${this.apiUrl}/books/all/`);
  }

  // Мой список
  getMyBooks() {
    return this.http.get(`${this.apiUrl}/my-books/`);
  }

  getUserBook(id: number) {
    return this.http.get(`${this.apiUrl}/my-books/${id}/`);
  }

  addToMyList(bookId: number) {
    return this.http.post(`${this.apiUrl}/my-books/`, { book_id: bookId });
  }

  updateUserBook(id: number, data: any) {
    return this.http.put(`${this.apiUrl}/my-books/${id}/`, data);
  }

  patchUserBook(id: number, data: any) {
    return this.http.patch(`${this.apiUrl}/my-books/${id}/`, data);
  }

  deleteUserBook(id: number) {
    return this.http.delete(`${this.apiUrl}/my-books/${id}/`);
  }

  // Reviews
  getReviews() {
    return this.http.get(`${this.apiUrl}/reviews/`);
  }

  getBookReviews(bookId: number) {
    return this.http.get(`${this.apiUrl}/books/${bookId}/reviews/`);
  }

  createReview(data: any) {
    return this.http.post(`${this.apiUrl}/reviews/`, data);
  }

  getProfile() {
    return this.http.get(`${this.apiUrl}/profile/`);
  }

  updateProfile(data: any) {
    return this.http.patch(`${this.apiUrl}/profile/`, data);
  }

  // Badges
  getBadges() {
    return this.http.get(`${this.apiUrl}/badges/`);
  }
}