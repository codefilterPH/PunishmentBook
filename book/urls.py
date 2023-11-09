from django.urls import path
from . import views  # Import the view function from the appropriate location
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/all-violation-page/', permanent=False), name='root_redirect'),
    path('all-violation-page/', views.all_violation_page, name='all_violation_page'),
    path('view-violation-page/<int:pk>/', views.view_violation_page, name='view_violation_page'),

    path('submission-page/', views.submission_page, name='submission_page'),
    path('submitted-offense-dt/', views.submitted_offense_dt, name='submitted_offense_dt'),

    path('submit-violation/', views.submit_function, name='submit_function'),
    path('get-imposed-by-whom-dt/', views.get_imposed_by_whom_dt, name='get_imposed_by_whom_dt'),
    path('get-violations-dt/', views.get_violations_dt, name='get_violations_dt'),
    path('get-punishments-dt/', views.get_punishments_dt, name='get_punishments_dt'),
    path('get-personnel/', views.get_personnel, name='get_personnel'),
    path('get-place-omission/', views.place_of_omission, name='place_of_omission'),
    path('get-resolutions/<int:pk>/', views.get_resolutions, name='place_of_omission'),
]
