import csv
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title

User = get_user_model()


DIR = settings.STATICFILES_DIRS[0] / 'data'
MODEL_TO_FILE = [
    (User, 'users.csv', {}),
    (Category, 'category.csv', {}),
    (Genre, 'genre.csv', {}),
    (Title, 'titles.csv', {'category': Category}),
    (GenreTitle, 'genre_title.csv', {}),
    (Review, 'review.csv', {'author': User}),
    (Comment, 'comments.csv', {'author': User}),
]


class Command(BaseCommand):
    help = "Loads data from static/data/*.csv"
    logger = logging.getLogger('main')

    def handle(self, *args, **options):
        for model, filepath, related in MODEL_TO_FILE:
            with open(DIR / filepath, encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.logger.log(logging.WARNING, f'Loading {filepath}')
                for row in reader:
                    for key, value in row.items():
                        if key in related:
                            row[key] = related[key].objects.get(pk=value)
                    model.objects.create(**row)
