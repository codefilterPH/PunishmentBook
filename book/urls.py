from django.urls import path
from . import views  # Import the view function from the appropriate location

urlpatterns = [
    path('submission-page/', views.submission_page, name='submission_page'),
    path('personnel-violation-page/', views.personnel_violation_page, name='personnel_with_violations'),
    path('submitted-offense-dt/', views.submitted_offense_dt, name='submitted_offense_dt'),


    path('offense-by-personnel-page/', views.offense_by_personnel_page, name='offense_by_personnel_page'),



    path('submit-violation/', views.submit_function, name='submit_function'),
    path('get-imposed-by-whom-dt/', views.get_imposed_by_whom_dt, name='get_imposed_by_whom_dt'),
    path('get-violations-dt/', views.get_violations_dt, name='get_violations_dt'),
    path('get-punishments-dt/', views.get_punishments_dt, name='get_punishments_dt'),
    path('get-personnel/', views.get_personnel, name='get_personnel'),
    path('get-place-omission/', views.place_of_omission, name='place_of_omission'),


]
