from django.db import models

class SensorData(models.Model):
    datetime = models.CharField(max_length=128, default='2024-01-01 00:00:00')
    device_id = models.CharField(max_length=128)
    datapoint = models.CharField(max_length=32)
    value = models.FloatField()
    timestamp = models.DateTimeField() 

    def __str__(self):
        return f"{self.device_id} - {self.datapoint}: {self.value}"
