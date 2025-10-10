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
    path('api/export-pdf/<int:session_id>/', views.export_pdf, name='export_pdf'),
    path('api/export-full-report-pdf/<int:session_id>/', views.export_full_report_pdf, name='export_full_report_pdf'),
    path('api/cancel-task/<int:session_id>/', views.cancel_task, name='cancel_task'),
    path('api/progress-stream/<int:session_id>/', views.progress_stream, name='progress_stream'),
]
