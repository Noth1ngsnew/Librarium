from django.core.management.base import BaseCommand
from books.models import Badge


class Command(BaseCommand):
    help = 'Seed initial badge data'

    def handle(self, *args, **kwargs):
        badges = [
            {'name': 'Книжный червь', 'icon': '📚', 'condition_key': 'first_book'},
            {'name': 'В кураже', 'icon': '🔥', 'condition_key': 'five_books'},
            {'name': 'Преданный читатель', 'icon': '🏆', 'condition_key': 'ten_books'},
            {'name': 'Библиотекарь', 'icon': '🏛️', 'condition_key': 'fifty_books'},

            {'name': 'Шерлок', 'icon': '🔍', 'condition_key': 'detective_fan'},
            {'name': 'Путешественник во времени', 'icon': '🚀', 'condition_key': 'sci_fi_fan'},
            {'name': 'Магистр магии', 'icon': '🧙', 'condition_key': 'fantasy_fan'},

            {'name': 'Критик', 'icon': '✍️', 'condition_key': 'first_review'},
            {'name': 'Полуночник', 'icon': '🌙', 'condition_key': 'night_reader'},
            {'name': 'Марафонец', 'icon': '🏃', 'condition_key': 'finished_in_one_day'},
        ]
        for data in badges:
            _, created = Badge.objects.get_or_create(
                condition_key=data['condition_key'],
                defaults=data,
            )
            label = 'created' if created else 'already exists'
            self.stdout.write(f"  {data['icon']}  {data['name']} — {label}")
        self.stdout.write(self.style.SUCCESS('\nBadges seeded successfully!'))
