from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
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
from .serializers import ThreadListSerializer, ThreadSerializer, CommentSerializer

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


@api_view(['GET'])
def thread_list(request):
    threads = Thread.objects.all()
    serializer = ThreadListSerializer(threads, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_thread(request, book_pk):
    book = Book.objects.get(pk=book_pk)
    serializer = ThreadSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(book=book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def thread_detail(request, thread_pk):
    thread = Thread.objects.annotate(num_of_comments=Count('comments')).get(pk=thread_pk)
    if request.method == 'GET':
        serializer = ThreadSerializer(thread)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ThreadSerializer(thread, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        thread.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def create_comment(request, thread_pk):
    thread = Thread.objects.get(pk=thread_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(thread=thread)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def comment_detail(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# @login_required
# def create(request):
#     if request.method == "POST":
#         form = BookForm(request.POST, request.FILES)
#         if form.is_valid():
#             book = form.save(commit=False)
#             book.user =request.user
#             wiki_summary = process_wikipedia_info(book)

#             author_info, author_works = generate_author_gpt_info(
#                 book, wiki_summary
#             )
#             book.author_info = author_info
#             book.author_works = author_works
#             book.save()

#             audio_script = generate_audio_script(book, wiki_summary)

#             audio_file_path = create_tts_audio(book, audio_script)
#             if audio_file_path:
#                 book.audio_file = audio_file_path
#                 book.save()

#             return redirect("books:detail", book.pk)
#     else:
#         form = BookForm()
#     context = {"form": form}
#     return render(request, "books/create.html", context)

# # @login_required
# def detail(request, pk):
#     book = Book.objects.get(pk=pk)
#     threadform = ThreadForm()
#     threads = book.thread_set.all()
#     context = {
#         "book": book,
#         "threads": threads,
#         'threadform': threadform,
#     }
#     return render(request, "books/detail.html", context)

# @login_required
# def update(request, pk):
#     book = Book.objects.get(pk=pk)
#     if request.method == "POST":
#         form = BookForm(request.POST, request.FILES, instance=book)
#         if form.is_valid():
#             form.save()
#             return redirect("books:detail", pk)
#     else:
#         form = BookForm(instance=book)
#     context = {
#         "form": form,
#         "book": book,
#     }
#     return render(request, "books/update.html", context)

# @login_required
# def delete(request, pk):
#     book = Book.objects.get(pk=pk)
#     if request.user == book.user:
#         book.delete()
#         return redirect("books:index")

