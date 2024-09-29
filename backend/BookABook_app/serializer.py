from rest_framework import serializers
from .models import User, Book,Genre


class UserSerializer(serializers.ModelSerializer):
    favorite_books = serializers.SlugRelatedField(
        slug_field='title',  # 通过书籍的title字段来建立关联
        queryset=Book.objects.all(),
        many=True,  # 因为是多对多关系
        required=False,  # 如果这个字段不是必须的
        allow_null=True  # 允许null值
    )
    favorite_genres = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Genre.objects.all(),
        required=False,
        allow_null=True
    )
    class Meta:
        model = User
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(
        slug_field='name',  # 使用Genre的name字段来关联
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genres']