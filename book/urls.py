from django.urls import path
from . import views  # Import the view function from the appropriate location

urlpatterns = [
    path('get-personnel/', views.get_personnel, name='get_personnel'),
    path('book/', views.punishment_book, name='punishment_book'),
    path('get-offense/', views.get_offense, name='get_offense'),
]
