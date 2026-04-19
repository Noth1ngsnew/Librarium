import { Component, inject, signal, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { BookService } from '../../services/book.service';

@Component({
  selector: 'app-badges',
  imports: [CommonModule],
  templateUrl: './badges.html',
  styleUrl: './badges.css'
})
export class Badges implements OnInit {
  private bookService = inject(BookService);
  private router = inject(Router);

  badges = signal<any[]>([]);

  ngOnInit() {
    this.loadBadges();
  }

  loadBadges() {
    this.bookService.getBadges().subscribe({
      next: (res: any) => this.badges.set(res),
      error: () => this.router.navigate(['/login'])
    });
  }

  goBack() {
    this.router.navigate(['/books']);
  }
}