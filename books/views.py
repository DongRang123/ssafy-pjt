from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Count
from .models import Category, Book, Thread, Comment
from .serializers import CategorylistSerializer,BooklistSerializer,BookSerializer
from .forms import BookForm,ThreadForm
from .utils import (
    process_wikipedia_info,
    generate_author_gpt_info,
    generate_audio_script,
    create_tts_audio,
    create_ai_image,
)
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST


@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorylistSerializer(categories,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def book_list(request):
    books = Book.objects.all()
    serializer = BooklistSerializer(books,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def book_detail(request,book_pk):
    books = Book.objects.annotate(num_of_threads=Count('threads')).get(pk=book_pk)
    serializer = BookSerializer(books)
    return Response(serializer.data)

