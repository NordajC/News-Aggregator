from rest_framework import serializers
from .models import Article
from .models import CustomUser


from rest_framework import serializers

class ArticleSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id','newsapi_id', 'title', 'category', 'category_name')

    def get_category_name(self, article):
        return article.category.name if article.category else None


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username','email', 'date_of_birth', 'profile_image', 'favorite_categories')