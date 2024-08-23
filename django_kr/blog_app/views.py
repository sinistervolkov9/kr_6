from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BlogPost
from .forms import BlogPostForm


class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog_app/blog_list.html'
    context_object_name = 'blogs'


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_app/blog_detail.html'
    context_object_name = 'blog'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.views += 1
        obj.save()
        return obj


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    template_name = 'blog_app/blog_form.html'
    form_class = BlogPostForm
    success_url = reverse_lazy('blog_app:blog_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog_app/blog_form.html'
    success_url = reverse_lazy('blog_app:blog_list')

    def test_func(self):
        blog = self.get_object()
        return self.request.user.is_superuser or blog.user == self.request.user


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    success_url = reverse_lazy('blog_app:blog_list')

    def test_func(self):
        blog = self.get_object()
        return self.request.user.is_superuser or blog.user == self.request.user
