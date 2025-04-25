from django.db import models
from django.conf import settings


class Category(models.Model):
    CATEGORY_CHOICES = [
        ('LITERATURE', '소설/시/희곡'),
        ('ECONOMY', '경제/경영'),
        ('DEVELOPMENT', '자기계발'),
        ('HUMANITY', '인문/교양'),
        ('SCIENCE', '과학'),
        ('HOBBY', '취미/실용'),
        ('MINORS', '어린이/청소년'),
    ]

    name = models.CharField(
        max_length=100,
        unique=True,
        choices=CATEGORY_CHOICES,
        help_text = '도서 종류를 선택해주세요.',
        verbose_name='카테고리',
        )

    def __str__(self):
        return self.get_name_display()
    

class Book(models.Model):
    # user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     related_name='books',
    #     verbose_name='등록한 사용자',
    #     on_delete=models.CASCADE,
    # )
    title = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    isbn = models.TextField()
    description = models.TextField()
    cover = models.ImageField(upload_to='book_covers/', blank=True)
    publisher = models.TextField()
    pub_date = models.TextField()
    author = models.TextField()
    customer_review_rank = models.IntegerField()


    # author_info = models.TextField(blank=True)
    # author_works = models.CharField(max_length=50, blank=True)
    
    # audio_file = models.FileField(upload_to="tts/", blank=True, null=True)
    
    
# 특정 도서에 대한 게시글
class Thread(models.Model):
    # user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    #     verbose_name='작성자',
    # )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='해당 도서', related_name='threads')
    title = models.CharField(max_length=100, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    reading_date = models.DateField(blank=True, verbose_name='독서일')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # cover_img = models.ImageField(upload_to="thread_covers/", blank=True, null=True)
    # like_users = models.ManyToManyField(
    #     settings.AUTH_USER_MODEL,
    #     related_name='liked_threads',
    #     blank=True,
    #     verbose_name='좋아요한 사용자'
    # )

    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, verbose_name="스레드 댓글", related_name="comments")
    content = models.TextField(verbose_name="내용")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)