from django.urls import path
from . import views

urlpatterns = [
    # Аутентификация (Function-Based Views)
    path('auth/register/', views.register_view, name='register'),
    path('auth/login/',    views.login_view,    name='login'),
    path('auth/logout/',   views.logout_view,   name='logout'),

    # Книги (Class-Based Views)
    path('books/', views.BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),

    # Логи чтения и Отзывы
    path('logs/',    views.ReadingLogListCreateView.as_view(), name='reading-logs'),
    path('reviews/', views.ReviewListCreateView.as_view(),     name='reviews'),

    # Достижения (Баджи)
    path('badges/', views.UserBadgeListView.as_view(), name='user-badges'),
]