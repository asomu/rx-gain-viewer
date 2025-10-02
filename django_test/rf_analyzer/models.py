"""
RF Analyzer Django Models
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class MeasurementSession(models.Model):
    """
    Measurement session (one analysis task)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='measurement_sessions')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    grid_config = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.user.username}"


class MeasurementFile(models.Model):
    """
    Uploaded SnP file
    """
    session = models.ForeignKey(MeasurementSession, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='measurements/%Y/%m/%d/')
    filename = models.CharField(max_length=255)
    file_size = models.IntegerField()
    main_band = models.CharField(max_length=50, blank=True, db_index=True)
    ca_label = models.CharField(max_length=100, blank=True, db_index=True)
    port_label = models.CharField(max_length=100, blank=True, db_index=True)
    condition = models.CharField(max_length=50, blank=True)
    is_parsed = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['main_band', 'ca_label', 'port_label']

    def __str__(self):
        return self.filename
