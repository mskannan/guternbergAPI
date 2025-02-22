from django.http import JsonResponse
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Q
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Book,BooksView
from itertools import zip_longest

@extend_schema(
    summary="Get a list of books",
    description="Retrieve books with pagination, search, and filtering.",
    parameters=[
        OpenApiParameter(name="limit", description="Number of books per page", required=False, type=int),
        OpenApiParameter(name="offset", description="Starting index for pagination", required=False, type=int),
        OpenApiParameter(name="search", description="Search by book title", required=False, type=str),
        OpenApiParameter(name="media_type", description="Filter by media type", required=False, type=str),
    ],
    responses={200: "application/json"},
)

@api_view(['GET'])
def book_list(request): 
    
    limit = int(request.GET.get('limit', 25))
    offset = int(request.GET.get('offset', 0))
    search_query = request.GET.get('search', '')
    media_type_filter = request.GET.get('media_type', '')

    books = BooksView.objects.all()

    # Search by title
    if search_query:
        books = books.filter(title__icontains=search_query)

    # Filter by media_type
    if media_type_filter:
        books = books.filter(media_type=media_type_filter)

    total_books = books.count()
    paginator = Paginator(books, limit) 
    page_number = (offset // limit) + 1

    try:
        current_page = paginator.page(page_number)
    except:
        return JsonResponse({"error": "Invalid page number"}, status=400)

    # books_json = [
    #     {"title": book.title, "media_type": book.media_type, "download_count": book.download_count}
    #     for book in current_page
    # ]
    books_json = generatejsonstruct(current_page)

    # Next & Previous Links
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
    books_json = []
    for book in books:
        authornamedata = book.author_name
        birthdate = book.birth_year
        deathdate = book.death_year
        mimedata = book.mime_type
        urldata = book.url

        author_list=[]
        
        for name, birth, death in zip_longest(authornamedata, birthdate, deathdate, fillvalue=None):
            author_list.append({
                "name": name,
                "birth_year": birth,
                "death_year": death
            })
        
        formatlist =[]
        for k in range(len(mimedata)): 
            cache_dict = {}
            cache_dict[mimedata[k]]= urldata[k]
            formatlist.append(cache_dict)
        
        books_json.append({
            "booktitle": book.booktitle,
            "authors": author_list,
            "subjects": [sub for sub in book.subjects],
            "bookshelves": [bookshelve for bookshelve in book.bookshelves],
            "languages": [lang for lang in book.languages],
            "formats": formatlist,
        })
    return books_json 



def testapi(request): 
    books = BooksView.objects.all()[:5]
    books_json = []
    for book in books:
        authornamedata = book.author_name
        birthdate = book.birth_year
        deathdate = book.death_year
        mimedata = book.mime_type
        urldata = book.url

        author_list=[]
        
        for name, birth, death in zip_longest(authornamedata, birthdate, deathdate, fillvalue=None):
            author_list.append({
                "name": name,
                "birth_year": birth,
                "death_year": death
            })
        
        formatlist =[]
        for k in range(len(mimedata)): 
            cache_dict = {}
            cache_dict[mimedata[k]]= urldata[k]
            formatlist.append(cache_dict)
        
        books_json.append({
            "booktitle": book.booktitle,
            "authors": author_list,
            "subjects": [sub for sub in book.subjects],
            "bookshelves": [bookshelve for bookshelve in book.bookshelves],
            "languages": [lang for lang in book.languages],
            "formats": formatlist,
        })
    return JsonResponse(books_json, safe=False)