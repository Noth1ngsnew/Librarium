import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  imports: [FormsModule, CommonModule],
  templateUrl: './login.html',
  styleUrl: './login.css'
})
export class Login {
  private auth = inject(AuthService);
  private router = inject(Router);

  isRegister = signal(false);
  error = signal('');

  formData = {
    username: '',
    email: '',
    password: ''
  };

  toggleMode() {
    this.isRegister.set(!this.isRegister());
    this.error.set('');
  }

  submit() {
    if (this.isRegister()) {
      this.auth.register(this.formData).subscribe({
        next: (res: any) => {
          this.auth.saveTokens(res.access, res.refresh);
          this.router.navigate(['/books']);
        },
        error: (err) => {
          this.error.set(err.error?.username?.[0] || 'Registration failed.');
        }
      });
    } else {
      this.auth.login(this.formData).subscribe({
        next: (res: any) => {
          this.auth.saveTokens(res.access, res.refresh);
          this.router.navigate(['/books']);
        },
        error: () => {
          this.error.set('Invalid username or password.');
        }
      });
    }
  }
}