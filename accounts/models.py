# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # 관심 장르
    interested_genres = models.ManyToManyField(
        'books.Category',
        related_name='interested_users',
        blank=True,
        verbose_name='관심 장르'
    )

    # 성별: 선택지 제공 (M/F)
    GENDER_CHOICES = [
        ('M', '남성'),
        ('F', '여성'),
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
        verbose_name='성별',
    )

    # 나이 (빈 값 허용)
    age = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='나이',
    )

    # 주간 평균 독서 시간
    weekly_avg_reading_time = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='주간 평균 독서 시간',
    )

    # 연간 독서량
    annual_reading_amount = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='연간 독서량',
    )

    # 프로필 사진
    profile_img = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True,
        verbose_name='프로필 사진',
    )

    # 팔로우
    followings = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True,
        verbose_name='팔로우',
    )

    # def get_favorite_categories_display(self):
    #     return self.favorite_categories.split(',') if self.favorite_categories else []

    def __str__(self):
        return self.username
    