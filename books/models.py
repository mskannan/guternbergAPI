from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    media_type = models.CharField(max_length=50)
    download_count = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    

class BooksView(models.Model):
    booktitle = models.CharField(max_length=255, primary_key=True)
    gut_book_id =  models.TextField(null=True, blank=True)
    author_name = models.TextField(null=True, blank=True)
    birth_year = models.TextField(null=True, blank=True)
    death_year = models.TextField(null=True, blank=True)
    subjects = models.TextField(null=True, blank=True)
    bookshelves = models.TextField(null=True, blank=True)
    languages = models.TextField(null=True, blank=True)
    mime_type = models.TextField(null=True, blank=True)
    url = models.TextField(null=True, blank=True)

    class Meta:
        managed = False  # Prevent Django from managing this table
        db_table = "books_view"  # Link to the existing Postgres view
