import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private http = inject(HttpClient);
  private router = inject(Router);
  private apiUrl = 'http://localhost:8000/api';

  register(data: any) {
    return this.http.post(`${this.apiUrl}/auth/register/`, data);
  }

  login(data: any) {
    return this.http.post(`${this.apiUrl}/auth/login/`, data);
  }

  logout() {
    const refresh = localStorage.getItem('refresh_token');
    return this.http.post(`${this.apiUrl}/auth/logout/`, { refresh });
  }

  saveTokens(access: string, refresh: string) {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
  }

  clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  isLoggedIn(): boolean {
    return !!localStorage.getItem('access_token');
  }
}