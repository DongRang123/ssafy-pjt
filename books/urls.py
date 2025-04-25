from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "books"
urlpatterns = [
    path("category/", views.category_list),
    path("", views.book_list),
    path("<int:book_pk>/", views.book_detail),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
