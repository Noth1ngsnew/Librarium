from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

"Позволяет быстро увидеть все книги, который читает пользователь"
class BookManager(models.Manager):
    def by_status(self, user, status):
        return self.filter(owner=user, status=status)


class Book(models.Model):
    STATUS_CHOICES = [
        ('reading', 'Reading'),
        ('finished', 'Finished'),
        ('want_to_read', 'Want to Read'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='want_to_read')
    current_page = models.PositiveIntegerField(default=0)
    total_pages = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = BookManager()

    def __str__(self):
        return self.title


class ReadingLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_logs')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='logs')
    status = models.CharField(max_length=20, choices=Book.STATUS_CHOICES)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} — {self.book.title} ({self.status})"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.book.title}"


class Badge(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=255)
    condition_key = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge')

    def __str__(self):
        return f"{self.user.username} — {self.badge.name}"
