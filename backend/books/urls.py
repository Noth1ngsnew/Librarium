from django.urls import path
from . import views

urlpatterns = [
    # авторизация
    path('auth/register/', views.register_view, name='register'),
    path('auth/login/',    views.login_view,    name='login'),
    path('auth/logout/',   views.logout_view,   name='logout'),

    # профиль юзера
    path('profile/', views.ProfileView.as_view(), name='profile'),

    # каталог книг и возможность удалить много книг из общего списка
    path('books/all/', views.AllBooksView.as_view(), name='all-books'),
    path('books/bulk-delete/', views.BulkDeleteBooksView.as_view(), name='bulk-delete-books'),
    path('books/<int:book_id>/reviews/', views.BookReviewsView.as_view(), name='book-reviews'),

    # список юзера, т.е его книг (my lish)
    path('my-books/',          views.UserBookListCreateView.as_view(), name='user-book-list'),
    path('my-books/<int:pk>/', views.UserBookDetailView.as_view(),     name='user-book-detail'),

    # отзывы
    path('reviews/', views.ReviewListCreateView.as_view(),     name='reviews'),
    path('logs/',    views.ReadingLogListCreateView.as_view(), name='logs'),

    # награды
    path('badges/', views.UserBadgeListView.as_view(), name='user-badges'),
]