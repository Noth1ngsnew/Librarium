# Librarium

A web application for tracking your reading activity. Users can add books, set reading statuses, write notes and reviews.

**Stack:** Angular + Django REST Framework  
**Practice Lesson:** Monday 14-16

---

## Group Members

| Name | 
|------|
| Kuanyshbek Bauyrzhanuly | 
| Danial Skabekov         | 
| Ramazan Khassanov       | 

---

## About the Project

Book Tracker allows users to manage their personal reading list. Each user can add books, track their current reading status, and leave personal notes or reviews.

**Core models:** `User`, `Book`, `ReadingLog`, `Review`

---

## Features

- JWT-based authentication (register, login, logout)
- Add and manage books with title, author, genre, and description
- Set reading status: *Reading*, *Finished*, *Want to Read*
- Write personal notes and reviews per book
- View and filter your reading history

---

## Tech Stack

### Frontend (Angular)
- Angular 17+ with standalone components
- `[(ngModel)]` for form bindings
- `HttpClient` + HTTP interceptor for JWT
- Angular Router with named routes
- `@for` / `@if` for dynamic rendering

### Backend (Django + DRF)
- Django REST Framework
- Token-based authentication
- `serializers.Serializer` and `ModelSerializer`
- Function-Based Views (FBV) and Class-Based Views (CBV)
- CORS configured via `django-cors-headers`
- Full CRUD for `Book` model

---

## Project Structure

```
book-tracker/
├── frontend/          # Angular application
│   └── src/
│       ├── app/
│       │   ├── components/
│       │   ├── services/
│       │   ├── interceptors/
│       │   └── app.routes.ts
│       └── ...
├── backend/           # Django project
│   ├── books/         # Main app
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   └── config/
├── postman/
│   └── book_tracker.postman_collection.json
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
| GET / PUT / DELETE | `/api/books/<id>/` | Retrieve, update, or delete a book |
| GET / POST | `/api/logs/` | Reading log entries |
| GET / POST | `/api/reviews/` | User reviews |

Full request/response examples are available in the Postman collection: `postman/book_tracker.postman_collection.json`

---

## Requirements Coverage

| Requirement | Status |
|-------------|--------|
| 4+ models | `User`, `Book`, `ReadingLog`, `Review` |
| 2+ ForeignKey relationships | `Book → User`, `Review → Book`, `ReadingLog → Book` |
| 2+ FBV with DRF decorators | Auth endpoints |
| 2+ CBV with APIView | Book and Review views |
| 2+ `serializers.Serializer` | Login, registration |
| 2+ `ModelSerializer` | Book, Review |
| Full CRUD for one model | `Book` |
| JWT auth | Login, logout, interceptor |
| CORS configured | `django-cors-headers` |
| 4+ `(click)` events | Add book, delete, update status, submit review |
| 4+ `[(ngModel)]` bindings | Login form, book form, review form |
| 3+ named routes | `/books`, `/books/:id`, `/login`, `/profile` |
| Angular Service with HttpClient | `BookService`, `AuthService` |
| Error handling | API error messages shown in UI |
