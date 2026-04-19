import { Component, inject, signal, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BookService } from '../../services/book.service';

@Component({
  selector: 'app-profile',
  imports: [CommonModule, FormsModule],
  templateUrl: './profile.html',
  styleUrl: './profile.css'
})
export class Profile implements OnInit {
  private bookService = inject(BookService);
  private router = inject(Router);

  profile = signal<any>(null);
  goalInput = signal(0);
  saved = signal(false);

  ngOnInit() {
    this.loadProfile();
  }

  loadProfile() {
    this.bookService.getProfile().subscribe({
      next: (res: any) => {
        this.profile.set(res);
        this.goalInput.set(res.reading_goal);
      },
      error: () => this.router.navigate(['/login'])
    });
  }

  saveGoal() {
    this.bookService.updateProfile({ reading_goal: this.goalInput() }).subscribe({
      next: (res: any) => {
        this.profile.update(p => ({ ...p, reading_goal: res.reading_goal }));
        this.saved.set(true);
        setTimeout(() => this.saved.set(false), 2000);
      }
    });
  }

  getGoalProgress(): number {
    const goal = this.profile()?.reading_goal;
    const done = this.profile()?.stats?.finished_this_year;
    if (!goal) return 0;
    return Math.min(Math.round((done / goal) * 100), 100);
  }

  goBack() {
    this.router.navigate(['/books']);
  }
}