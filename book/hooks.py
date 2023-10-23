from wagtail import hooks
from django.urls import path
from book.views import punishment_book

@hooks.register('register_admin_urls')
def register_punishment_book():
    return [
        path('book/', punishment_book, name='punishment_book'),
    ]
