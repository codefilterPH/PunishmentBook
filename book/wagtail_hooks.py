from wagtail import hooks
from django.urls import path
from . import views


@hooks.register('register_admin_urls')
def register_punishment_book():
    return [
        path('', views.punishment_book, name='punishment_book'),
    ]
