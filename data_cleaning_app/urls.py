from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload'),
    path('options/', views.cleaning_options, name='options'),
    path('report/', views.cleaning_report, name='report'),
    path('download/', views.download_cleaned_file, name='download'),
]
