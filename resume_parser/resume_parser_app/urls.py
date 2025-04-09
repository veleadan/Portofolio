from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_resume, name='upload_resume'),  # Root page URL
    path('results/', views.results, name='results'),  # Results page URL
]
