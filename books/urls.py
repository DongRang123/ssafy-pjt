from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "books"
urlpatterns = [
    path("category/", views.category_list),
    path("", views.book_list),
    path("<int:book_pk>/", views.book_detail),
    path("threads/", views.thread_list),
    path("threads/<int:thread_pk>/", views.thread_detail),
    path("<int:book_pk>/threads/", views.create_thread),
    path("threads/<int:thread_pk>/comments/", views.create_comment),
    path("comments/<int:comment_pk>/", views.comment_detail),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# path("", views.index, name="index"),
# path("create/", views.create, name="create"),
# path("<int:pk>/", views.detail, name="detail"),
# path("<int:pk>/update/", views.update, name="update"),
# path("<int:pk>/delete/", views.delete, name="delete"),