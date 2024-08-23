from django.core.exceptions import PermissionDenied
from .forms import ClientForm, MessageForm, MailingForm, MailingManagerForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from .models import Client, Mailing, Message, Attempt
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView, ListView, DetailView
from blog_app.models import BlogPost
import random


class HomeTemplateView(TemplateView):
    """Контроллер главной страницы"""

    template_name = 'mailing_app/base.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        # client_count = len(Client.objects.filter(user=self.request.user.pk))
        # newsletter_count = len(Mailing.objects.filter(user=self.request.user.pk))
        # active_newsletter = len(Mailing.objects.filter(user=self.request.user.pk, status='started'))

        client_count = Client.objects.count()
        newsletter_count = Mailing.objects.count()
        active_newsletter = len(Mailing.objects.filter(status='started'))

        blogs = BlogPost.objects.all()

        context['random_blogs'] = random.sample(list(blogs), min(3, len(blogs)))

        context['newsletter_count'] = newsletter_count
        context['client_count'] = client_count
        context['active_newsletter'] = active_newsletter

        context['is_home'] = self.request.path == reverse('newsletter:base')

        return context


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing_app/client_form.html'
    success_url = reverse_lazy('newsletter:client_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self):
        """Вывод клиентов пользователя"""
        # return super().get_queryset().filter(user=self.request.user)
        return super().get_queryset()


class ClientDetailView(DetailView):
    model = Client
    template_name = 'mailing_app/client_detail.html'
    context_object_name = 'client'


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing_app/client_form.html'
    success_url = reverse_lazy('newsletter:client_list')

    def test_func(self):
        client = self.get_object()
        return self.request.user.is_superuser or client.user == self.request.user


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('newsletter:client_list')

    def test_func(self):
        client = self.get_object()
        return self.request.user.is_superuser or client.user == self.request.user


# ----------------------------------------------------------------------------------------------------------------------

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing_app:message_list')

    def form_valid(self, form):
        """Добавление пользователя к сообщению"""
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        """Вывод сообщений пользователя"""
        # return super().get_queryset().filter(user=self.request.user)
        return super().get_queryset()


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailing_app/message_detail.html'
    context_object_name = 'message'


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('newsletter:message_list')

    def test_func(self):
        message = self.get_object()
        return self.request.user.is_superuser or message.user == self.request.user


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('newsletter:message_list')

    def test_func(self):
        message = self.get_object()
        return self.request.user.is_superuser or message.user == self.request.user


# -----------------------------------------------------------------------------------------------------------------------


class NewsLetterCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing_app:mailing_list')

    def form_valid(self, form):
        """Добавление пользователя к рассылке"""
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class NewsLetterDetailView(DetailView):
    model = Mailing
    template_name = 'mailing_app/mailing_detail.html'
    context_object_name = 'mailing'


class NewsLetterListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_queryset(self):
        """Вывод рассылок пользователя либо всех рассылок для модератора"""
        if self.request.user.has_perm('newsletter.view_newsletter'):
            return super().get_queryset()
        # return super().get_queryset().filter(user=self.request.user)
        return super().get_queryset()


class NewsLetterUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('newsletter:mailing_list')

    def test_func(self):
        mailing = self.get_object()
        return self.request.user.is_superuser or mailing.user == self.request.user

    def get_form_class(self):
        user = self.request.user
        if user == self.object.user or user.is_superuser:
            return MailingForm
        if user.has_perm('mailing_app.can_set_status'):
            return MailingManagerForm
        raise PermissionDenied


class NewsLetterDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('newsletter:mailing_list')

    def test_func(self):
        mailing = self.get_object()
        return self.request.user.is_superuser or mailing.user == self.request.user


def status_newsletter(request, pk):
    """Контроллер смены статуса рассылки"""
    newsletter = Mailing.objects.get(pk=pk)
    if request.user == newsletter.user or request.user.has_perm('newsletter.set_status'):
        if newsletter.status == 'created':
            newsletter.status = 'started'
            newsletter.save()
        elif newsletter.status == 'started':
            newsletter.status = 'created'
            newsletter.save()
        else:
            newsletter.status = 'started'
            newsletter.save()
    return redirect(reverse('newsletter:mailing_list'))


def finish_newsletter(request, pk):
    newsletter = Mailing.objects.get(pk=pk)
    if request.user == newsletter.user or request.user.has_perm('newsletter.set_status'):
        newsletter.status = 'completed'
        newsletter.save()
    return redirect(reverse('newsletter:mailing_list'))


# ----------------------------------------------------------------------------------------------------------------------


class LogListView(LoginRequiredMixin, ListView):
    model = Attempt

    def get_queryset(self):
        """Вывод логов пользователя"""
        return super().get_queryset().filter(user=self.request.user)
