import { Routes } from '@angular/router';
import { Login } from './components/login/login';
import { BookList } from './components/book-list/book-list';
import { BookDetail } from './components/book-detail/book-detail';
import { MyList } from './components/my-list/my-list';
import { Badges } from './components/badges/badges';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: Login },
  { path: 'books', component: BookList },
  { path: 'books/:id', component: BookDetail },
  { path: 'my-list', component: MyList },
  { path: 'badges', component: Badges },
];