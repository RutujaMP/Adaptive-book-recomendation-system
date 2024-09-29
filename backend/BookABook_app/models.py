from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255,unique=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    genres = models.ManyToManyField('Genre', related_name='books')
    # description = models.TextField(blank=True, null=True)
    num_pages = models.IntegerField(blank=True, null=True)
    # additional_info = models.IntegerField(blank=True, null=True)  # Previously 'nan'

    class Meta:
        db_table = 'books'

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True) 

    def save(self, *args, **kwargs):
        if not self.slug:  # 如果slug字段为空
            self.slug = slugify(self.name)  # 自动生成slug
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'genres'
    
    def __str__(self) -> str:

        return str(self.name)


class User(AbstractUser):
    # name = models.CharField(max_length=100)
    # age = models.PositiveIntegerField(null=True, blank=True)
    # gender = models.CharField(max_length=10, choices=(('male', 'Male'), ('female', 'Female')), blank=True)
    favorite_books = models.ManyToManyField(Book, blank=True)
    favorite_genres = models.ManyToManyField(Genre, blank=True)
    
    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        unique_together = ('user', 'book')
        db_table = 'ratings'

    def __str__(self):
        return f'{self.user} rated {self.book}: {self.rating}'
    

class UserMoods(models.Model):
    user_id = models.IntegerField()  # Assuming user_id can be represented as text
    mood1 = models.TextField(null=True, blank=True)
    mood2 = models.TextField(null=True, blank=True)
    mood3 = models.TextField(null=True, blank=True)
    mood4 = models.TextField(null=True, blank=True)
    mood5 = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
    # Set mood1 to the new mood value (latest value)
        self.mood1 = self.mood5

    # If all mood columns are already filled, shift the values
        if all(getattr(self, f'mood{i}') for i in range(1, 6)):
            self.mood5 = self.mood4
            self.mood4 = self.mood3
            self.mood3 = self.mood2
            self.mood2 = self.mood1
        super(UserMoods, self).save(*args, **kwargs)

    class Meta:
        db_table = 'user_moodTrack'

    def __str__(self):
        return f"UserMoods for user {self.user_id}"

