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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='measurement_sessions', null=True, blank=True)  # Phase 1: nullable
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    grid_config = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        username = self.user.username if self.user else 'Anonymous'
        return f"{self.name} - {username}"


class MeasurementFile(models.Model):
    """
    Uploaded SnP or CSV file
    """
    FILE_TYPE_CHOICES = [
        ('snp', 'SnP File'),
        ('csv', 'CSV File'),
    ]

    session = models.ForeignKey(MeasurementSession, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='measurements/%Y/%m/%d/')
    filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES, default='csv')
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


class MeasurementData(models.Model):
    """
    Raw measurement data point (from CSV or SnP)
    Stores key columns from consolidated CSV format
    """
    session = models.ForeignKey(MeasurementSession, on_delete=models.CASCADE, related_name='data_points')

    # Configuration columns (from CSV)
    cfg_band = models.CharField(max_length=20, db_index=True)  # B1, B41, n75, etc.
    cfg_lna_gain_state = models.CharField(max_length=10, db_index=True)  # G0_H, G0_L, G1-G5
    cfg_active_port_1 = models.CharField(max_length=10, db_index=True)  # ANT1, ANT2, ANTL
    cfg_active_port_2 = models.CharField(max_length=10)  # RXOUT1-4

    # Debug/CA information
    debug_nplexer_bank = models.CharField(max_length=100, db_index=True)  # CA combination
    active_rf_path = models.CharField(max_length=10, db_index=True)  # S0706, S0705, etc.

    # Measurement data
    frequency_mhz = models.FloatField(db_index=True)  # Frequency in MHz
    gain_db = models.FloatField()  # Gain in dB

    # Additional metadata (optional, can store JSON for other columns)
    extra_data = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['cfg_band', 'cfg_lna_gain_state', 'cfg_active_port_1', 'frequency_mhz']
        indexes = [
            models.Index(fields=['cfg_band', 'cfg_lna_gain_state', 'cfg_active_port_1']),
            models.Index(fields=['cfg_band', 'debug_nplexer_bank']),
            models.Index(fields=['active_rf_path', 'frequency_mhz']),
        ]

    def __str__(self):
        return f"{self.cfg_band} {self.cfg_lna_gain_state} {self.cfg_active_port_1} @ {self.frequency_mhz}MHz"
