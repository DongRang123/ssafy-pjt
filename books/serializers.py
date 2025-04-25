from .models import Category, Book, Thread, Comment
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    pass


class BookSerializer(serializers.ModelSerializer):
    pass


class CommentSerializer(serializers.ModelSerializer):
    
    class ThreadTitleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Thread
            fields = ('title',)
    
    thread = ThreadTitleSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = '__all__'


class ThreadListSerializer(serializers.ModelSerializer):
    
    class BookTitleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Book
            fields = ('title',)
    
    book = BookTitleSerializer(read_only=True)
    
    class Meta:
        model = Thread
        fields = ('id', 'title', 'book',)


class ThreadSerializer(serializers.ModelSerializer):
    
    class BookTitleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Book
            fields = ('title',)
    
    comments = CommentSerializer(many=True, read_only=True)
    num_of_comments = serializers.SerializerMethodField()
    book = BookTitleSerializer(read_only=True)
    
    class Meta:
        model = Thread
        fields = '__all__'
        
    def get_num_of_comments(self, obj):
        return obj.num_of_comments

