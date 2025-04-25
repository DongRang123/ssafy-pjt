from .models import Category, Book, Thread, Comment
from rest_framework import serializers


class CategorylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BooklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id','title','author','isbn','cover',)

class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    num_of_threads = serializers.SerializerMethodField()

    threads = ThreadSerializer(many=True,read_only=True)
    category = CategorylistSerializer(read_only=True)
    class Meta:
        model = Book
        fields = ('id','category','threads','num_of_threads',
                  
            'title', 'description','isbn', 'cover', 'publisher', 'pub_date', 'author',
            )
        

    def get_num_of_threads(self,obj):
        return obj.num_of_threads


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
