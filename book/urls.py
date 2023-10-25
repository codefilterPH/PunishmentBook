from django.urls import path
from . import views  # Import the view function from the appropriate location

urlpatterns = [
    path('submission-page/', views.submission_page, name='submit_offense'),
    path('personnel-violation-page/', views.personnel_violation_page, name='personnel-with-violations'),
    path('submitted-offense-dt/', views.get_submitted_offense_dt, name='get_submitted_offense_dt'),
    path('get-personnel/', views.get_personnel, name='get_personnel'),
    path('get-offense/', views.get_offense, name='get_offense'),
    path('get-punishments/', views.get_punishments, name='get_punishments'),
    path('get-place-omission/', views.place_of_omission, name='place_of_omission'),
]
