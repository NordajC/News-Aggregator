from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from .forms import CustomUserCreationForm
from django.shortcuts import render
import requests
from .models import Category
from newsapi import NewsApiClient
from .models import Article
from .models import CustomUser
from .models import Comment
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from rest_framework.generics import ListAPIView
from .serializers import ArticleSerializer
from .serializers import CustomUserSerializer
from rest_framework.permissions import IsAuthenticated
from django.views.generic import View 
from rest_framework.decorators import api_view
from django.http import HttpResponseRedirect
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
import json


api = NewsApiClient(api_key='5cb563123d2d4abea49a38e3e3124466')

def main_spa(request: HttpRequest) -> HttpResponse:
    create_default_categories()
    return render(request, 'api/spa/index.html', {})

def signup(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  
            return redirect('main_spa') 
    else:
        form = UserCreationForm()

    return render(request, 'api/spa/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'api/spa/login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('http://localhost:5173')
        else:
            return render(request, self.template_name, {
                'error_message': 'Invalid username or password.'
            })

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)



def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return HttpResponseRedirect('http://localhost:5173')
    else:
        form = CustomUserCreationForm()

    return render(request, 'api/spa/signup.html', {'form': form})

def create_default_categories():
    category_names = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
    for name in category_names:
        Category.objects.get_or_create(name=name)



def fetch_articles_from_newsapi():
    for category_name in ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']:
        top_headlines = api.get_top_headlines(category=category_name, language='en', country='us')
        articles_data = top_headlines.get('articles', [])
        
        category, created = Category.objects.get_or_create(name=category_name)
        
        for article_data in articles_data:
            Article.objects.get_or_create(
                newsapi_id=article_data['url'],
                defaults={
                    'title': article_data['title'],
                    'category': category
                }
            )




@login_required
def show_articles(request):
    favorite_categories = request.user.favorite_categories.all()

    if favorite_categories.exists():
        articles = Article.objects.filter(category__in=favorite_categories)
    else:
        articles = Article.objects.all()

    return render(request, 'api/spa/articles.html', {'articles': articles})




@api_view(['GET'])
def get_user_profile(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    user_profile = request.user
    serializer = CustomUserSerializer(user_profile)

    return JsonResponse(serializer.data)


@csrf_exempt
@login_required
def update_user_profile(request):
    if request.method == 'POST':
        user_profile = CustomUser.objects.get(id=request.user.id)
 
        user_profile.email = request.POST.get('email', user_profile.email)
        user_profile.date_of_birth = request.POST.get('date_of_birth', user_profile.date_of_birth)
        favorite_categories_ids = json.loads(request.POST.get('favorite_categories'))
        favorite_categories = Category.objects.filter(id__in=favorite_categories_ids)
        user_profile.favorite_categories.set(favorite_categories)
 
        profile_image_file = request.FILES.get('profile_image')
        if profile_image_file:
            buffer = BytesIO(profile_image_file.read())
            profile_image = InMemoryUploadedFile(buffer, None, profile_image_file.name, 'image/jpeg', buffer.tell(), None)
            user_profile.profile_image = profile_image
 
        user_profile.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


@csrf_exempt  
@login_required
@require_POST  
def post_comment(request, article_id):
    try:
        data = json.loads(request.body)  
        content = data.get('content')
        parent_id = data.get('parent_id')  

        
        if not content:
            return JsonResponse({'status': 'error', 'message': 'Content cannot be empty'}, status=400)

        article = Article.objects.get(id=article_id)

        comment = Comment.objects.create(
            article=article,
            author=request.user,
            content=content,
            parent_id=parent_id if parent_id else None
        )

        return JsonResponse({'status': 'success', 'comment_id': comment.id})

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except ObjectDoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Article not found'}, status=404)
    except Exception as e:
        print(f"Error in post_comment: {e}")
        return JsonResponse({'status': 'error', 'message': 'An error occurred'}, status=500)

@login_required
def get_comments(request, article_id):
    comments = Comment.objects.filter(article_id=article_id, parent__isnull=True)
    comments_data = [{
        'id': comment.id,
        'content': comment.content,
        'author': comment.author.username,
        'replies': [
            {
                'id': reply.id,
                'content': reply.content,
                'author': reply.author.username
            } for reply in comment.replies.all()
        ]
    } for comment in comments]

    return JsonResponse({'comments': comments_data})

@csrf_exempt  
@login_required
@require_http_methods(["PUT"])  
def edit_comment(request, comment_id):
    
    data = json.loads(request.body)

    try:
        comment = Comment.objects.get(id=comment_id, author=request.user)
        new_content = data.get('content')  
        if new_content:
            comment.content = new_content
            comment.save()
            return JsonResponse({'status': 'success', 'comment_id': comment.id})
        else:
            return JsonResponse({'status': 'error', 'message': 'No content provided'}, status=400)
    except Comment.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Comment not found or access denied'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid data format'}, status=400)

@csrf_exempt
@login_required
def delete_comment(request, comment_id):
    if request.method == 'POST':
        try:
            comment = Comment.objects.get(id=comment_id, author=request.user)
            comment.delete()
            return JsonResponse({'status': 'success'})
        except Comment.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Comment not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def vue_app(request):
    return render(request, '../frontend/index.html')

@csrf_exempt
@require_POST
def logout_view(request):
    logout(request)
    return JsonResponse({'status': 'success'})

class ArticleListView(APIView):
    permission_classes = []

    def get(self, request, format=None):
        
        favorite_categories = request.user.favorite_categories.all()

        if favorite_categories:
            articles = Article.objects.filter(category__in=favorite_categories)
        else:
            articles = Article.objects.all()

        serializer = ArticleSerializer(articles, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

def category_list(request):
    categories = Category.objects.all().values('id', 'name')
    return JsonResponse(list(categories), safe=False)

