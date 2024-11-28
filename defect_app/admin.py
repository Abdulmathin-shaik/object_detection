from django.contrib import admin
from .models import DefectDetection

@admin.register(DefectDetection)
class DefectDetectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial_number', 'model_type', 'inspection_date')
    list_filter = ('model_type', 'inspection_date')
    search_fields = ('name', 'serial_number')
