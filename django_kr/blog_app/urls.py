from django.urls import path
from .apps import BlogAppConfig
from .views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = BlogAppConfig.name

urlpatterns = [
    path('blog_list/', BlogListView.as_view(), name='blog_list'),
    path('blog_create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog_detail/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog_edit/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),
    path('blog_delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),
]
