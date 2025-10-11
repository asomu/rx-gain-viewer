from django.contrib import admin
from .models import MeasurementSession, MeasurementFile, MeasurementData


@admin.register(MeasurementSession)
class MeasurementSessionAdmin(admin.ModelAdmin):
    """Admin interface for MeasurementSession"""
    list_display = ['name', 'user', 'file_count', 'data_point_count', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at', 'file_count', 'data_point_count']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'user')
        }),
        ('Configuration', {
            'fields': ('grid_config',),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('file_count', 'data_point_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def file_count(self, obj):
        """Display number of files"""
        return obj.files.count()
    file_count.short_description = 'Files'
    
    def data_point_count(self, obj):
        """Display number of data points"""
        return obj.data_points.count()
    data_point_count.short_description = 'Data Points'


@admin.register(MeasurementFile)
class MeasurementFileAdmin(admin.ModelAdmin):
    """Admin interface for MeasurementFile"""
    list_display = ['filename', 'session', 'file_type', 'main_band', 'ca_label', 'port_label', 'is_parsed', 'file_size_kb', 'uploaded_at']
    list_filter = ['file_type', 'main_band', 'is_parsed', 'uploaded_at']
    search_fields = ['filename', 'session__name', 'main_band', 'ca_label', 'port_label']
    readonly_fields = ['filename', 'file_size', 'file_size_kb', 'uploaded_at']
    date_hierarchy = 'uploaded_at'
    
    fieldsets = (
        ('File Information', {
            'fields': ('session', 'file', 'filename', 'file_type', 'file_size_kb')
        }),
        ('Parsed Metadata', {
            'fields': ('main_band', 'ca_label', 'port_label', 'condition', 'is_parsed')
        }),
        ('Timestamps', {
            'fields': ('uploaded_at',),
            'classes': ('collapse',)
        }),
    )
    
    def file_size_kb(self, obj):
        """Display file size in KB"""
        return f"{obj.file_size / 1024:.2f} KB"
    file_size_kb.short_description = 'File Size'
    
    actions = ['mark_as_parsed', 'mark_as_unparsed']
    
    def mark_as_parsed(self, request, queryset):
        """Bulk action: mark files as parsed"""
        updated = queryset.update(is_parsed=True)
        self.message_user(request, f"{updated} files marked as parsed")
    mark_as_parsed.short_description = "Mark selected files as parsed"
    
    def mark_as_unparsed(self, request, queryset):
        """Bulk action: mark files as unparsed"""
        updated = queryset.update(is_parsed=False)
        self.message_user(request, f"{updated} files marked as unparsed")
    mark_as_unparsed.short_description = "Mark selected files as unparsed"


@admin.register(MeasurementData)
class MeasurementDataAdmin(admin.ModelAdmin):
    """Admin interface for MeasurementData"""
    list_display = ['session', 'cfg_band', 'cfg_lna_gain_state', 'cfg_active_port_1', 'cfg_active_port_2', 'active_rf_path', 'frequency_mhz', 'gain_db']
    search_fields = ['session__name', 'cfg_band', 'debug_nplexer_bank', 'active_rf_path']
    readonly_fields = ['created_at']
    list_per_page = 100  # Limit pagination for performance
    
    # Removed list_filter to avoid distinct() issue with large datasets
    # Users can use search instead
    
    fieldsets = (
        ('Session', {
            'fields': ('session',)
        }),
        ('Configuration', {
            'fields': ('cfg_band', 'cfg_lna_gain_state', 'cfg_active_port_1', 'cfg_active_port_2')
        }),
        ('RF Path', {
            'fields': ('debug_nplexer_bank', 'active_rf_path')
        }),
        ('Measurement', {
            'fields': ('frequency_mhz', 'gain_db')
        }),
        ('Extra Data', {
            'fields': ('extra_data',),
            'classes': ('collapse',)
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['export_to_csv']
    
    def export_to_csv(self, request, queryset):
        """Bulk action: export selected data to CSV"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="measurement_data.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Session', 'Band', 'LNA State', 'Port1', 'Port2', 'RF Path', 'Frequency (MHz)', 'Gain (dB)'])
        
        for obj in queryset:
            writer.writerow([
                obj.session.name,
                obj.cfg_band,
                obj.cfg_lna_gain_state,
                obj.cfg_active_port_1,
                obj.cfg_active_port_2,
                obj.active_rf_path,
                obj.frequency_mhz,
                obj.gain_db
            ])
        
        return response
    export_to_csv.short_description = "Export selected data to CSV"
