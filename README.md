# guternbergAPI
A django project with Rest API to list the table datas in JSON format


Django API with PostgreSQL - Setup Guide

Prerequisites
Ensure you have the following installed:
- Python (>= 3.x)
- PostgreSQL (>= 12.x)
- pip & virtualenv
- Git

--------------------------------------------

1️⃣ Clone the Repository
git clone <your-repo-url>
cd <your-project-folder>

--------------------------------------------

2️⃣ Set Up a Virtual Environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

--------------------------------------------

3️⃣ Install Dependencies
pip install -r requirements.txt

--------------------------------------------

4️⃣ Configure PostgreSQL Database

🛠 Create Database
1. Open PostgreSQL shell (psql) or use pgAdmin.
2. Run the following commands:

CREATE DATABASE mydb;
CREATE USER myuser WITH PASSWORD 'mypassword';
ALTER ROLE myuser SET client_encoding TO 'utf8';
ALTER ROLE myuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;

🛠 Update settings.py
Modify DATABASES in settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

--------------------------------------------

5️⃣ Apply Migrations
python manage.py migrate

--------------------------------------------

6️⃣ Create Superuser (Optional)
python manage.py createsuperuser
Follow the prompts to set up an admin account.

--------------------------------------------

7️⃣ Run the Django Server
python manage.py runserver
Open http://127.0.0.1:8000/ in your browser.

--------------------------------------------

8️⃣ API Documentation (Optional)
If using drf-spectacular, generate the schema:
python manage.py spectacular --color --file schema.yml
View API docs at:
- Swagger UI: http://127.0.0.1:8000/docs/ 

--------------------------------------------


------------------------------------------------

Create a Database View in PostgreSQL

Execute the SQL query in your PostgreSQL database:

CREATE VIEW books_view AS
SELECT
    bb.title AS booktitle,
    bb.gutenberg_id AS gut_book_id,  
    array_agg(DISTINCT ba.name) AS author_name,
    array_agg(DISTINCT ba.birth_year) AS birth_year,
    array_agg(DISTINCT ba.death_year) AS death_year, 
    array_agg(DISTINCT bs.name) AS subjects,
    array_agg(DISTINCT bbshelf.name) AS bookshelves,
    array_agg(DISTINCT bl.code) AS languages,
    array_agg(DISTINCT bf.mime_type) AS mime_type,
    array_agg(DISTINCT bf.url) AS url
FROM
  books_book AS bb
LEFT JOIN books_book_authors AS bba ON bba.book_id = bb.id
LEFT JOIN books_author AS ba ON ba.id = bba.author_id
LEFT JOIN books_book_languages AS bbl ON bbl.book_id = bb.id
LEFT JOIN books_language AS bl ON bl.id = bbl.language_id
LEFT JOIN books_book_subjects AS bbs ON bbs.book_id = bb.id
LEFT JOIN books_subject AS bs ON bs.id = bbs.subject_id
LEFT JOIN books_book_bookshelves AS bbb ON bbb.book_id = bb.id
LEFT JOIN books_bookshelf AS bbshelf ON bbshelf.id = bbb.bookshelf_id
LEFT JOIN books_format AS bf ON bf.book_id = bb.id
GROUP BY bb.title, bb.gutenberg_id;

------------------------------------------------