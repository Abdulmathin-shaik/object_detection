from django.db import models

class DefectDetection(models.Model):
    name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    model_type = models.CharField(max_length=20)
    inspection_date = models.DateTimeField(auto_now_add=True)
    defect_results = models.JSONField()  # Store defect types and counts
    image = models.ImageField(upload_to='defect_images/')

    def __str__(self):
        return f"Inspection: {self.serial_number} by {self.name}"

    class Meta:
        ordering = ['-inspection_date']
