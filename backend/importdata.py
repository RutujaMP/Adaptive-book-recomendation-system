import csv
import django
import os
from django.db import IntegrityError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookABook_project.settings')
django.setup()

from BookABook_app.models import Book, Genre


# conn = sqlite3.connect('db_test.sqlite3')
# c = conn.cursor()

def import_book_from_csv(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8-sig') as csv_file:
        reader = csv.DictReader(csv_file)
        print("CSV Headers: ", reader.fieldnames)
        counter = 0
        for row in reader:
            if counter >= 10000:
                break
            try:
                genre_names = row['genre'].split(',')
                genre_instances = []

                for name in genre_names:
                    # print(f"current genre name is {name}")
                    genre, created = Genre.objects.get_or_create(name=name.strip().lower())
                    genre_instances.append(genre)
            except IntegrityError as e:
                print(f"An error occured for genre: '{name}, book name is {row['title']}'. Error:{e}")

            book, created = Book.objects.get_or_create(
                title=row['title'],
                defaults={
                    'author': row['author'],
                    'num_pages': int(float(row['num_pages']))
                }
            )

            for genre in genre_instances:
                book.genres.add(genre)

            counter += 1


if __name__ == "__main__":
    csv_file_path = r"data/books.csv".replace('\\', '/')
    import_book_from_csv(csv_file_path=csv_file_path)
