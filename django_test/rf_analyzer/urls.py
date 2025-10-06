"""
RF Analyzer URL Configuration
"""

from django.urls import path
from . import views

app_name = 'rf_analyzer'

urlpatterns = [
    path('', views.index, name='index'),
    path('viewer/<int:session_id>/', views.viewer, name='viewer'),
    path('api/chart/<int:session_id>/', views.get_chart_data, name='chart_data'),
]
