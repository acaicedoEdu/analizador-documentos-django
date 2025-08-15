from django.urls import path
from .views import AnalyzeArchiveView


urlpatterns = [
    path('analizar/', AnalyzeArchiveView.as_view()),
] 
