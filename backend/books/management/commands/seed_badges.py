from django.core.management.base import BaseCommand
from books.models import Badge


class Command(BaseCommand):
    help = 'Seed initial badge data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update existing badges with new names',
        )

    def handle(self, *args, **kwargs):
        badges = [
            {'name': 'Bookworm', 'icon': '📚', 'condition_key': 'first_book', 'description': 'Finish your first book'},
            {'name': 'On Fire', 'icon': '🔥', 'condition_key': 'five_books', 'description': 'Finish 5 books'},
            {'name': 'Devoted Reader', 'icon': '🏆', 'condition_key': 'ten_books', 'description': 'Finish 10 books'},
            {'name': 'Librarian', 'icon': '🏛️', 'condition_key': 'fifty_books', 'description': 'Finish 50 books'},
            {'name': 'Sherlock', 'icon': '🔍', 'condition_key': 'detective_fan', 'description': 'Read a detective book'},
            {'name': 'Time Traveler', 'icon': '🚀', 'condition_key': 'sci_fi_fan', 'description': 'Read a sci-fi book'},
            {'name': 'Master of Magic', 'icon': '🧙', 'condition_key': 'fantasy_fan', 'description': 'Read a fantasy book'},
            {'name': 'Critic', 'icon': '✍️', 'condition_key': 'first_review', 'description': 'Write your first review'},
            {'name': 'Night Owl', 'icon': '🌙', 'condition_key': 'night_reader', 'description': 'Read late at night'},
            {'name': 'Marathoner', 'icon': '🏃', 'condition_key': 'finished_in_one_day', 'description': 'Finish a book in one day'},
        ]

        for data in badges:
            if kwargs['update']:
                badge, created = Badge.objects.update_or_create(
                    condition_key=data['condition_key'],
                    defaults={'name': data['name'], 'icon': data['icon']},
                )
                label = 'created' if created else 'updated'
            else:
                badge, created = Badge.objects.get_or_create(
                    condition_key=data['condition_key'],
                    defaults=data,
                )
                label = 'created' if created else 'already exists'

            self.stdout.write(f"  {data['icon']}  {data['name']} — {label}")

        self.stdout.write(self.style.SUCCESS('\nBadges seeded successfully!'))