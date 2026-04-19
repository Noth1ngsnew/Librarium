from django.contrib import admin
from .models import Book, UserBook, ReadingLog, Review, Badge, UserBadge

admin.site.register(Book)
admin.site.register(UserBook)
admin.site.register(ReadingLog)
admin.site.register(Review)
admin.site.register(Badge)
admin.site.register(UserBadge)