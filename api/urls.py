"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

#api urls
from django.urls import path
from .views import main_spa, signup, CustomLoginView, show_articles, get_user_profile, update_user_profile, vue_app, logout_view, ArticleListView 
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', main_spa, name='main_spa'),
    path('signup/', signup, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('articles/', show_articles, name='articles'),
    path('user/profile/', views.get_user_profile, name='get_user_profile'),
    path('user/profile/update/', update_user_profile, name='update_user_profile'),
    path('articles/<int:article_id>/post_comment/', views.post_comment, name='post_comment'),
    path('articles/<int:article_id>/get_comments/', views.get_comments, name='get_comments'),
    path('articles/comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('comments/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('app/', vue_app, name='vue_app'),
    path('logout/', logout_view, name='logout'),
    path('articleData/', ArticleListView.as_view(), name='article-list'),
    path('user/profile/json/', views.get_user_profile, name='get_user_profile_json'),
    path('categories/', views.category_list, name='category_list'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
