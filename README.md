# Librarium

A web application for tracking your reading activity. Users can add books, set reading statuses, write notes and reviews, track reading progress, and earn badges.

**Stack:** Angular + Django REST Framework  
**Practice Lesson:** Monday 14-16

---

## Group Members

| Name |
|------|
| Kuanyshbek Bauyrzhanuly |
| Danial Skabekov |
| Ramazan Khassanov |

---

## About the Project

Librarium allows users to manage their personal reading list. Each user can add books, track their current reading status, leave personal notes or reviews, monitor reading progress with a progress bar, and earn badges based on their reading activity. Book covers are automatically fetched from the Open Library API.

**Core models:** `User`, `Book`, `ReadingLog`, `Review`, `Badge`, `UserBadge`

---

## Features

- JWT-based authentication (register, login, logout)
- Add and manage books with title, author, genre, and description
- Automatic book cover fetching via Open Library API
- Set reading status: *Reading*, *Finished*, *Want to Read*
- Track reading progress with current page and total pages
- Write personal notes and reviews per book
- View and filter your reading history
- Earn badges based on reading achievements

---

## Badges

| Badge | Icon | Condition |
|-------|------|-----------|
| Bookworm | 📚 | Finish your first book |
| On a Roll | 🔥 | Finish 5 books |
| Devoted Reader | 🏆 | Finish 10 books |

---

## Tech Stack

### Frontend (Angular)
- Angular 17+ with standalone components
- `[(ngModel)]` for form bindings
- `HttpClient` + HTTP interceptor for JWT
- Angular Router with named routes
- `@for` / `@if` for dynamic rendering
- Open Library API integration for book covers

### Backend (Django + DRF)
- Django REST Framework
- Token-based authentication via `djangorestframework-simplejwt`
- `serializers.Serializer` and `ModelSerializer`
- Function-Based Views (FBV) and Class-Based Views (CBV)
- CORS configured via `django-cors-headers`
- Full CRUD for `Book` model
- Automatic badge awarding on reading milestones

---

## Project Structure

```
librarium/
├── frontend/                   # Angular application
│   └── src/
│       ├── app/
│       │   ├── components/
│       │   │   ├── login/
│       │   │   ├── book-list/
│       │   │   ├── book-detail/
│       │   │   ├── my-list/
│       │   │   └── badges/
│       │   ├── services/
│       │   │   ├── auth.service.ts
│       │   │   └── book.service.ts
│       │   ├── interceptors/
│       │   │   └── jwt.interceptor.ts
│       │   └── app.routes.ts
│       └── ...
├── backend/                    # Django project
│   ├── books/                  # Main app
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
source venv/bin/activate  # Windows: venv\Scripts\activate
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

The app will be available at `http://localhost:4200`.  
The API runs at `http://localhost:8000`.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | Obtain JWT token |
| POST | `/api/auth/logout/` | Logout |
| GET / POST | `/api/books/` | List or create books |
| GET / PUT / PATCH / DELETE | `/api/books/<id>/` | Retrieve, update, or delete a book |
| GET / POST | `/api/logs/` | Reading log entries |
| GET / POST | `/api/reviews/` | User reviews |
| GET | `/api/badges/` | Get current user badges |

Full request/response examples are available in the Postman collection: `postman/book_tracker.postman_collection.json`

---

## Requirements Coverage

| Requirement | Status | Details |
|-------------|--------|---------|
| 4+ models | ✅ | `User`, `Book`, `ReadingLog`, `Review`, `Badge`, `UserBadge` |
| 1 custom model manager | ✅ | `BookManager.by_status()` |
| 2+ ForeignKey relationships | ✅ | `Book → User`, `Review → Book`, `ReadingLog → Book`, `UserBadge → User/Badge` |
| 2+ FBV with DRF decorators | ✅ | `register_view`, `login_view`, `logout_view` |
| 2+ CBV with APIView | ✅ | `BookListCreateView`, `BookDetailView`, `ReviewListCreateView`, `UserBadgeListView` |
| 2+ `serializers.Serializer` | ✅ | `LoginSerializer`, `RegisterSerializer` |
| 2+ `ModelSerializer` | ✅ | `BookSerializer`, `ReviewSerializer`, `ReadingLogSerializer`, `UserBadgeSerializer` |
| Full CRUD for one model | ✅ | `Book` |
| JWT auth | ✅ | Login, logout, interceptor |
| CORS configured | ✅ | `django-cors-headers` |
| Link objects to authenticated user | ✅ | `request.user` on Book and Review create |
| 4+ `(click)` events | ✅ | Add book, delete book, update status, submit review, update progress |
| 4+ `[(ngModel)]` bindings | ✅ | Login form, book form, review form, progress fields |
| 3+ named routes | ✅ | `/login`, `/books`, `/books/:id`, `/my-list`, `/badges` |
| Angular Service with HttpClient | ✅ | `BookService`, `AuthService` |
| Error handling | ✅ | API error messages shown in UI |
| Book covers | ✅ | Open Library API |
| Reading progress bar | ✅ | `current_page` / `total_pages` on Book |
| Badge system | ✅ | Auto-awarded on reading milestones |
