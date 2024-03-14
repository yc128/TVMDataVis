from django.db import models

# Create your models here.
class Benchmark(models.Model):
    RunId = models.CharField(max_length=255, primary_key=True)
    TOTAL_TASK_GRAPH_TIME = models.IntegerField(null=True)
    COPY_IN_TIME = models.IntegerField(null=True)
    TOTAL_DISPATCH_DATA_TRANSFER_TIME = models.IntegerField(null=True)
    COPY_OUT_TIME = models.IntegerField(null=True)
    TOTAL_KERNEL_TIME = models.IntegerField(null=True)
    TOTAL_DISPATCH_KERNEL_TIME = models.IntegerField(null=True)
    TOTAL_COPY_IN_SIZE_BYTES = models.IntegerField(null=True)
    TOTAL_COPY_OUT_SIZE_BYTES = models.IntegerField(null=True)
    DRIVER = models.CharField(max_length=255, null=True)
    METHOD = models.CharField(max_length=255, null=True)
    DEVICE_ID = models.CharField(max_length=255, null=True)
    DEVICE = models.CharField(max_length=255, null=True)
    TOTAL_COPY_IN_SIZE_BYTES_R = models.IntegerField(null=True)
    TASK_KERNEL_TIME = models.IntegerField(null=True)
