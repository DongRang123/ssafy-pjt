from django.shortcuts import render, redirect
from .models import Book, Thread
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


def index(request):
    books = Book.objects.all()
    context = {
        "books": books,
    }
    return render(request, "books/index.html", context)

@login_required
def create(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.user =request.user
            wiki_summary = process_wikipedia_info(book)

            author_info, author_works = generate_author_gpt_info(
                book, wiki_summary
            )
            book.author_info = author_info
            book.author_works = author_works
            book.save()

            audio_script = generate_audio_script(book, wiki_summary)

            audio_file_path = create_tts_audio(book, audio_script)
            if audio_file_path:
                book.audio_file = audio_file_path
                book.save()

            return redirect("books:detail", book.pk)
    else:
        form = BookForm()
    context = {"form": form}
    return render(request, "books/create.html", context)

# @login_required
def detail(request, pk):
    book = Book.objects.get(pk=pk)
    threadform = ThreadForm()
    threads = book.thread_set.all()
    context = {
        "book": book,
        "threads": threads,
        'threadform': threadform,
    }
    return render(request, "books/detail.html", context)

@login_required
def update(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect("books:detail", pk)
    else:
        form = BookForm(instance=book)
    context = {
        "form": form,
        "book": book,
    }
    return render(request, "books/update.html", context)

@login_required
def delete(request, pk):
    book = Book.objects.get(pk=pk)
    if request.user == book.user:
        book.delete()
        return redirect("books:index")

@login_required
@require_http_methods(['GET', 'POST'])
def thread_create(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == "POST":
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.book = book
            thread.user = request.user
            thread.cover_img = create_ai_image(thread.content)
            thread.save()
            return redirect("books:detail", pk=pk)
    else:
        form = ThreadForm()
    context={
        'form': form,
        'pk': pk,
    }
    return render(request,"books/thread_create.html",context)

# @login_required
@require_http_methods(['GET'])
def thread_detail(request, pk):
    thread= Thread.objects.get(pk=pk)
    context={
        'thread': thread,
    }
    return render(request,'books/thread_detail.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def thread_update(request, pk):
    thread = Thread.objects.get(pk=pk)
    if request.user == thread.user:
        if request.method == "POST":
            form = ThreadForm(request.POST, request.FILES, instance=thread)
            if form.is_valid():
                form.save()
                return redirect("books:detail", thread.book.pk)
        else:
            form = ThreadForm(instance=thread)
    else:
        return redirect('books:thread_detail', thread.pk)
    context = {
        "form": form,
        "thread": thread,
    }
    return render(request, "books/thread_update.html", context)

@login_required
@require_POST
def thread_delete(request, pk):
    thread = Thread.objects.get(pk=pk)
    if request.user == thread.user:
        thread.delete()
    return redirect("books:detail", thread.book.pk)

@login_required
def thread_likes(request,pk):
    thread = Thread.objects.get(pk=pk)
    if request.user in thread.like_users.all():
        thread.like_users.remove(request.user)
    else:
        thread.like_users.add(request.user)
    return redirect('books:thread_detail',pk)