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



class BookSerializer(serializers.ModelSerializer):


    class ThreadforbookSerializer(serializers.ModelSerializer):
        class Meta:
            model = Thread
            fields = ('id','title','content','reading_date')

    num_of_threads = serializers.SerializerMethodField()

    threads = ThreadforbookSerializer(many=True,read_only=True)
    category = CategorylistSerializer(read_only=True)
    class Meta:
        model = Book
        fields = ('id','category','threads','num_of_threads',
                  
            'title', 'description','isbn', 'cover', 'publisher', 'pub_date', 'author',
            )
        

    def get_num_of_threads(self,obj):
        return obj.num_of_threads
