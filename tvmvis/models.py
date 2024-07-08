from django.db import models


class Run(models.Model):
    RunID = models.AutoField(primary_key=True)
    DateTime = models.DateTimeField() # last modified time of output_profiler, or dateTime data in other place?
    CommitPoint = models.CharField(max_length=255) # can not relate
    Version = models.CharField(max_length=255) # can not relate
    Description = models.TextField() # can not relate


class Benchmark(models.Model):
    BenchmarkID = models.AutoField(primary_key=True)
    Run = models.ForeignKey(Run, on_delete=models.CASCADE)
    BenchmarkName = models.CharField(max_length=255, default="None")
    NumberOfIterations = models.IntegerField(default=-1)
    BenchmarkFlags = models.CharField(max_length=255, default="None")
    MTMD = models.IntegerField(default=-1)
    SizeType = models.IntegerField(default=0)
    SizeNumber = models.CharField(max_length=255, default=0)
    Dimension = models.IntegerField(default=0)


class TotalResults(models.Model):
    ResultID = models.AutoField(primary_key=True)
    Benchmark = models.ForeignKey(Benchmark, on_delete=models.CASCADE)
    TotalAverageTime = models.BigIntegerField(default=0)
    TotalMedianTime = models.BigIntegerField(default=0)
    TotalFirstIteration = models.BigIntegerField(default=0)
    TotalBest = models.BigIntegerField(default=0)
    TotalMinimum = models.BigIntegerField(default=0)
    TotalSpeedup = models.FloatField(default=0)


class TaskGraphResults(models.Model):
    TaskGraphID = models.AutoField(primary_key=True)
    Result = models.ForeignKey(TotalResults, on_delete=models.CASCADE)
    LastKernelTime = models.IntegerField(default=0)
    KernelAverage = models.IntegerField(default=0)
    Copy_IN = models.IntegerField(default=0)
    Copy_OUT = models.IntegerField(default=0)
    Compilation_Graal = models.IntegerField(default=0)
    Compilation_Driver = models.IntegerField(default=0)
    Dispatch_Kernel_Time = models.IntegerField(default=0)
    Dispatch_DataTransfers_Time = models.IntegerField(default=0)


class TaskResults(models.Model):
    TaskID = models.AutoField(primary_key=True)
    TaskGraphResult = models.ForeignKey(TaskGraphResults, on_delete=models.CASCADE)
    HardwareInfo = models.CharField(null=True, max_length=255)
    SoftwareInfo = models.CharField(null=True, max_length=255)
    KernelTime = models.IntegerField(default=0)
    CodeGenerationTime = models.IntegerField(default=0)
    DriverCompilationTime = models.IntegerField(default=0)
    PowerMetric = models.FloatField(null=True, blank=True)


class SoftwareConfiguration(models.Model): # Use result from versions.json
    SoftwareID = models.AutoField(primary_key=True)
    OSVersion = models.CharField(max_length=255, default="None")
    DriverVersion = models.CharField(max_length=255, default="None")
    JVMVersion = models.CharField(max_length=255, default="None")
    GCCVersion = models.CharField(max_length=255, default="None")
    MavenVersion = models.CharField(max_length=255, default="None")
    CmakeVersion = models.CharField(max_length=255, default="None")
    PythonVersion = models.CharField(max_length=255, default="None")


class HardwareConfiguration(models.Model):
    HardwareInfo = models.AutoField(primary_key=True)
    DeviceID = models.IntegerField(default=0)
    DeviceType = models.CharField(max_length=255, default="None")
    DeviceName = models.CharField(max_length=255, default="None")
    GlobalMemorySize = models.IntegerField(default=0)
    LocalMemorySize = models.IntegerField(default=0)
    GlobalThreadNumber = models.IntegerField(default=0)
    LocalThreadNumber = models.IntegerField(default=0)
    MaxFrequency = models.FloatField(default=0)
    ComputeUnits = models.IntegerField(default=0)
    DeviceExtensions = models.CharField(max_length=255, default="None")
    ComputeCapability = models.CharField(max_length=255, default="None")
    DevicePartitioning = models.CharField(max_length=255, default="None")
    MaxWorkItemDimension = models.IntegerField(default=0)
    UnifiedMemory = models.BooleanField(default=False)
    AtomicSupport = models.BooleanField(default=False)
    HalfPrecisionSupport = models.BooleanField(default=False)
    DoubleSupport = models.BooleanField(default=False)


