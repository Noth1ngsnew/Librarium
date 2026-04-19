# Librarium

A web application for tracking personal reading activity. Users can manage their book list, set reading statuses, write reviews, track progress by page, and earn achievement badges.

**Stack:** Angular 17 + Django REST Framework  
**Practice Lesson:** Monday 14–16

---

## Group Members

| Name |
|------|
| Kuanyshbek Bauyrzhanuly |
| Danial Skabekov |
| Ramazan Khassanov |

---

## About the Project

Librarium lets users manage a personal reading list. Each user can add books from the catalog, track reading status and current page, leave reviews with star ratings, view reading history through logs, and earn badges based on milestones. Book covers are fetched automatically from the Google Books and Open Library APIs.

**Core models:** `User`, `Book`, `UserBook`, `ReadingLog`, `Review`, `Badge`, `UserBadge`

---

## Features

- JWT-based authentication (register, login, logout with token blacklisting)
- Book catalog with genre filtering
- Add books to a personal reading list
- Set and update reading status: Reading, Finished, Want to Read
- Track reading progress by current page and total pages
- Write and view reviews with star ratings
- Reading history log with status change tracking
- Badge system with automatic awarding on reading milestones
- Automatic book cover fetching from Google Books API with localStorage caching
- User profile with reading statistics and yearly reading goal

---

## Badges

| Badge | Icon | Condition |
|-------|------|-----------|
| Bookworm | 📚 | Finish your first book |
| On Fire | 🔥 | Finish 5 books |
| Devoted Reader | 🏆 | Finish 10 books |

---

## Tech Stack

### Frontend — Angular 17

- Standalone components with modern control flow (`@if`, `@for`)
- Signals and `computed()` for reactive state management
- `HttpClient` with functional JWT interceptor
- Angular Router with named routes and lazy-ready structure
- `FormsModule` with `[(ngModel)]` bindings
- Google Books API integration with localStorage cover caching

### Backend — Django + DRF

- Django REST Framework with JWT via `djangorestframework-simplejwt`
- Token blacklisting on logout
- `Serializer` and `ModelSerializer` classes
- Function-based views (FBV) and class-based views (CBV) with `APIView`
- CORS configured via `django-cors-headers`
- Full CRUD for `Book` model
- Automatic badge awarding on reading milestones
- Management command for seeding badge data

---

## Project Structure

```
librarium/
├── frontend/
│   └── src/
│       └── app/
│           ├── components/
│           │   ├── login/
│           │   ├── book-list/
│           │   ├── book-detail/
│           │   ├── my-list/
│           │   ├── badges/
│           │   └── profile/
│           ├── services/
│           │   ├── auth.service.ts
│           │   └── book.service.ts
│           ├── interceptors/
│           │   └── jwt.interceptor.ts
│           └── app.routes.ts
├── backend/
│   ├── books/
│   │   ├── migrations/
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── seed_badges.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   └── config/
│       ├── settings.py
│       └── urls.py
├── postman/
│   └── book_tracker.postman_collection.json
├── requirements.txt
└── README.md
```

---

## Getting Started

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_badges
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
ng serve
```

The app runs at `http://localhost:4200`.  
The API runs at `http://localhost:8000`.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | Obtain JWT tokens |
| POST | `/api/auth/logout/` | Blacklist refresh token |
| GET | `/api/books/all/` | List all books in catalog |
| GET / POST | `/api/my-books/` | List or add user books |
| GET / PUT / PATCH / DELETE | `/api/my-books/<id>/` | Manage a specific user book |
| GET | `/api/books/<id>/reviews/` | Reviews for a specific book |
| GET / POST | `/api/reviews/` | User reviews |
| GET / POST | `/api/logs/` | Reading log entries |
| GET | `/api/badges/` | Current user badges |
| GET / PATCH | `/api/profile/` | User profile and reading goal |

Full request/response examples are available in the Postman collection: `postman/book_tracker.postman_collection.json`

---

## Requirements Coverage

| Requirement | Status | Details |
|-------------|--------|---------|
| 4+ models | Done | `User`, `Book`, `UserBook`, `ReadingLog`, `Review`, `Badge`, `UserBadge` |
| 2+ ForeignKey relationships | Done | `UserBook → Book/User`, `Review → Book/User`, `ReadingLog → Book/User`, `UserBadge → User/Badge` |
| 2+ FBV with DRF decorators | Done | `register_view`, `login_view`, `logout_view` |
| 2+ CBV with APIView | Done | `AllBooksView`, `UserBookListCreateView`, `UserBookDetailView`, `ReviewListCreateView`, `UserBadgeListView` |
| 2+ `serializers.Serializer` | Done | `LoginSerializer`, `RegisterSerializer` |
| 2+ `ModelSerializer` | Done | `BookSerializer`, `ReviewSerializer`, `ReadingLogSerializer`, `UserBadgeSerializer` |
| Full CRUD for one model | Done | `Book` and `UserBook` |
| JWT auth | Done | Login, logout with blacklist, interceptor |
| CORS configured | Done | `django-cors-headers` |
| Link objects to authenticated user | Done | `request.user` used in `UserBook`, `Review`, `ReadingLog` |
| 4+ `(click)` events | Done | Add book, delete, update status, submit review, update progress |
| 4+ `[(ngModel)]` bindings | Done | Login form, review form, goal input, progress input |
| 3+ named routes | Done | `/login`, `/books`, `/books/:id`, `/my-list`, `/badges`, `/profile` |
| Angular Service with HttpClient | Done | `BookService`, `AuthService` |
| Error handling | Done | API error messages displayed in UI |
| Book covers | Done | Google Books API with Open Library fallback |
| Reading progress bar | Done | `current_page` / `total_pages` |
| Badge system | Done | Auto-awarded on milestones via `award_badges()` |
