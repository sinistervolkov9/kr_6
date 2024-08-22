from .apps import MailingAppConfig
from django.urls import path
from .views import HomeTemplateView, ClientListView, ClientUpdateView, ClientDeleteView, MessageCreateView, \
    MessageListView, MessageUpdateView, MessageDeleteView, LogListView, NewsLetterDeleteView, NewsLetterCreateView, \
    NewsLetterListView, NewsLetterUpdateView, ClientCreateView, status_newsletter, finish_newsletter, \
    ClientDetailView, MessageDetailView, NewsLetterDetailView
from users.views import UserListView

app_name = MailingAppConfig.name

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='base'),

    path('user_list', UserListView.as_view(), name='user_list'),

    path('client_create', ClientCreateView.as_view(), name='client_create'),
    path('client_list', ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client/<int:pk>/edit/', ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),

    path('create_message', MessageCreateView.as_view(), name='create_message'),
    path('message_list', MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('edit_message/<int:pk>', MessageUpdateView.as_view(), name='edit_message'),
    path('delete_message/<int:pk>', MessageDeleteView.as_view(), name='delete_message'),

    path('create_mailing', NewsLetterCreateView.as_view(), name='create_mailing'),
    path('mailing_list', NewsLetterListView.as_view(), name='mailing_list'),
    path('mailing/<int:pk>/', NewsLetterDetailView.as_view(), name='mailing_detail'),
    path('edit_mailing/<int:pk>', NewsLetterUpdateView.as_view(), name='edit_mailing'),
    path('delete_mailing/<int:pk>', NewsLetterDeleteView.as_view(), name='delete_mailing'),

    path('status_mailing/<int:pk>', status_newsletter, name='status_mailing'),
    path('finish_mailing/<int:pk>', finish_newsletter, name='finish_mailing'),

    path('attempt_list', LogListView.as_view(), name='attempt_list'),
]
