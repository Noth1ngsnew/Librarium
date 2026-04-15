from django.contrib import admin
from .models import Book, ReadingLog, Review, Badge, UserBadge

# Registration 
admin.site.register(Book)
admin.site.register(ReadingLog)
admin.site.register(Review)
admin.site.register(Badge)
admin.site.register(UserBadge)