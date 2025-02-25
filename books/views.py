from django.http import JsonResponse
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Q
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Book, BooksView
from itertools import zip_longest

@extend_schema(
    summary="Get a list of books",
    description="Retrieve books with pagination, search, and filtering.",
    parameters=[
        OpenApiParameter(name="limit", description="Number of books per page", required=False, type=int),
        OpenApiParameter(name="offset", description="Starting index for pagination", required=False, type=int),
        OpenApiParameter(name="id", description="Search by book IDs (Eg: 1,2)", required=False, type=str),
        OpenApiParameter(name="title", description="Search by book Titles (Eg:A House of Pomegranates)", required=False, type=str),
        OpenApiParameter(name="topic", description="Search by book Topics (Eg: Children)", required=False, type=str),
        OpenApiParameter(name="author", description="Search by book Authors (Eg:Charles)", required=False, type=str),
        OpenApiParameter(name="mime_type", description="Search by book Mime Type (Eg:text/html,text/plain)", required=False, type=str),
        OpenApiParameter(name="languages", description="Search by book Languages (Eg: en,fr,fi)", required=False, type=str),
    ],
    responses={200: "application/json"},
)
@api_view(['GET'])
def book_list(request):  
    """
    View to retrieve a list of books with support for filtering, searching, and pagination.
    """
    
    # Get query parameters
    limit = int(request.GET.get('limit', 25))  # Number of books per page
    offset = int(request.GET.get('offset', 0))  # Starting index for pagination
    title_filter = request.GET.get('title', '')
    topic_filter = request.GET.get('topic', '')
    author_filter = request.GET.get('author', '')
    mime_filter = request.GET.get('mime_type', '')
    language_filter = request.GET.get('languages', '')
    book_id_filter = request.GET.get('id', '')

    books = BooksView.objects.all()  # Fetch all books from the view

    # Filtering by book ID
    if book_id_filter:
        book_ids = book_id_filter.split(',')
        books = books.filter(gut_book_id__in=book_ids)    
    
    # Filtering by Topic (subject or title match)
    if topic_filter:
        topic_filters = topic_filter.split(',')
        topicquery = Q()
        for topics in topic_filters:
            topicquery |= Q(subjects__icontains=topics)  
            topicquery |= Q(booktitle__icontains=topics)  
        books = books.filter(topicquery)

    # Filtering by Title
    if title_filter:
        title_filters = title_filter.split(',')
        titlequery = Q()
        for titles in title_filters:
            titlequery |= Q(booktitle__icontains=titles)  
        books = books.filter(titlequery)

    # Filtering by Author
    if author_filter:
        author_filters = author_filter.split(',')
        authorquery = Q()
        for authors in author_filters:
            authorquery |= Q(author_name__icontains=authors)  
        books = books.filter(authorquery)

    # Filtering by Mime Type
    if mime_filter:
        mime_filters = mime_filter.split(',')
        mimequery = Q()
        for mimes in mime_filters:
            mimequery |= Q(mime_type__icontains=mimes)  
        books = books.filter(mimequery)
    
    # Filtering by Language
    if language_filter:
        language_filters = language_filter.split(',')
        langquery = Q()
        for lang in language_filters:
            langquery |= Q(languages__icontains=lang)  
        books = books.filter(langquery)

    # Pagination setup
    total_books = books.count()
    paginator = Paginator(books, limit)  # Paginate results
    page_number = (offset // limit) + 1  # Determine current page number

    if total_books == 0:
        return JsonResponse({"Message": "Please try some other filter or search options"})

    try:
        current_page = paginator.page(page_number)
    except:
        return JsonResponse({"error": "Invalid page number"}, status=400)
 
    # Convert paginated books to JSON
    books_json = generatejsonstruct(current_page)

    # Generate next and previous page links
    next_offset = offset + limit if current_page.has_next() else None
    prev_offset = offset - limit if offset > 0 else None  

    next_link = request.build_absolute_uri(reverse("book-list") + f"?limit={limit}&offset={next_offset}") if next_offset else None
    prev_link = request.build_absolute_uri(reverse("book-list") + f"?limit={limit}&offset={prev_offset}") if prev_offset is not None else None

    return JsonResponse({
        "count": total_books,
        "next": next_link,
        "previous": prev_link,
        "results": books_json
    })


def generatejsonstruct(books):  
    """
    Helper function to convert book queryset into a structured JSON format.
    """
    books_json = []
    for book in books:
        authornamedata = book.author_name
        birthdate = book.birth_year
        deathdate = book.death_year
        mimedata = book.mime_type
        urldata = book.url

        author_list = []
        
        # Convert author data into list of dictionaries
        for name, birth, death in zip_longest(authornamedata, birthdate, deathdate, fillvalue=None):
            author_list.append({
                "name": name,
                "birth_year": birth,
                "death_year": death
            })
        
        # Convert format data into list of dictionaries
        formatlist = []
        for k in range(len(mimedata)): 
            formatlist.append({mimedata[k]: urldata[k]})
        
        books_json.append({
            "booktitle": book.booktitle,
            "authors": author_list,
            "subjects": list(book.subjects),  # Convert to list
            "bookshelves": list(book.bookshelves),
            "languages": list(book.languages),
            "formats": formatlist,
        })
    return books_json 


def testapi(request):  
    """
    Test API to retrieve first 5 books from BooksView and return sample JSON response.
    """
    books = BooksView.objects.all()[:5]
    books_json = []

    for book in books:
        authornamedata = book.author_name
        birthdate = book.birth_year
        deathdate = book.death_year
        mimedata = book.mime_type
        urldata = book.url

        author_list = []
        
        # Convert author data into structured JSON format
        for name, birth, death in zip_longest(authornamedata, birthdate, deathdate, fillvalue=None):
            author_list.append({
                "name": name,
                "birth_year": birth,
                "death_year": death
            })
        
        # Convert formats into list of dictionaries
        formatlist = []
        for k in range(len(mimedata)): 
            formatlist.append({mimedata[k]: urldata[k]})
        
        books_json.append({
            "booktitle": book.booktitle,
            "authors": author_list,
            "subjects": list(book.subjects),
            "bookshelves": list(book.bookshelves),
            "languages": list(book.languages),
            "formats": formatlist,
        })
    
    return JsonResponse(books_json, safe=False)
