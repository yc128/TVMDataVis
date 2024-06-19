from django.db import models


class Run(models.Model):
    RunID = models.AutoField(primary_key=True)
    DateTime = models.DateTimeField() # last modified time of output_profiler, or dateTime data in other place?
    CommitPoint = models.CharField(max_length=255) # can not relate
    LatestRelease = models.CharField(max_length=255) # can not relate
    Description = models.TextField() # can not relate


class Benchmark(models.Model): # can not relate
    BenchmarkID = models.AutoField(primary_key=True)
    Run = models.ForeignKey(Run, on_delete=models.CASCADE)
    BenchmarkName = models.CharField(max_length=255)
    NumberOfIterations = models.IntegerField()
    BenchmarkFlags = models.CharField(max_length=255)
    MTMD = models.IntegerField()
    SizeType = models.IntegerField()
    SizeNumber = models.CharField(max_length=255)
    Dimension = models.IntegerField()


class TotalResults(models.Model): # can not relate
    ResultID = models.AutoField(primary_key=True)
    Benchmark = models.ForeignKey(Benchmark, on_delete=models.CASCADE)
    TotalAverageTime = models.BigIntegerField()
    TotalMedianTime = models.BigIntegerField()
    TotalFirstIteration = models.BigIntegerField()
    TotalBest = models.BigIntegerField()
    TotalMinimum = models.BigIntegerField()
    TotalSpeedup = models.FloatField()


class TaskGraphResults(models.Model):
    TaskGraphID = models.AutoField(primary_key=True)
    Result = models.ForeignKey(TotalResults, on_delete=models.CASCADE)
    LastKernelTime = models.IntegerField()
    KernelAverage = models.IntegerField()
    Copy_IN = models.IntegerField()
    Copy_OUT = models.IntegerField()
    Compilation_Graal = models.IntegerField()
    Compilation_Driver = models.IntegerField()
    Dispatch_Kernel_Time = models.IntegerField()
    Dispatch_DataTransfers_Time = models.IntegerField()


class TaskResults(models.Model): # can not relate
    TaskID = models.AutoField(primary_key=True)
    TaskGraphResult = models.ForeignKey(TaskGraphResults, on_delete=models.CASCADE)
    HardwareInfo = models.CharField(max_length=255)
    SoftwareInfo = models.CharField(max_length=255)
    KernelTime = models.IntegerField()
    CodeGenerationTime = models.IntegerField()
    DriverCompilationTime = models.IntegerField()
    PowerMetric = models.FloatField(null=True, blank=True)


class SoftwareConfiguration(models.Model): # Use result from versions.json
    SoftwareID = models.AutoField(primary_key=True)
    OSVersion = models.CharField(max_length=255)
    DriverVersion = models.CharField(max_length=255)
    JVMVersion = models.CharField(max_length=255)
    GCCVersion = models.CharField(max_length=255)
    MavenVersion = models.CharField(max_length=255)
    CmakeVersion = models.CharField(max_length=255)
    PythonVersion = models.CharField(max_length=255)


class HardwareConfiguration(models.Model): # can not relate
    HardwareInfo = models.AutoField(primary_key=True)
    DeviceID = models.IntegerField()
    DeviceType = models.CharField(max_length=255)
    DeviceName = models.CharField(max_length=255)
    GlobalMemorySize = models.IntegerField()
    LocalMemorySize = models.IntegerField()
    GlobalThreadNumber = models.IntegerField()
    LocalThreadNumber = models.IntegerField()
    MaxFrequency = models.FloatField()
    ComputeUnits = models.IntegerField()
    DeviceExtensions = models.CharField(max_length=255)
    ComputeCapability = models.CharField(max_length=255)
    DevicePartitioning = models.CharField(max_length=255)
    MaxWorkItemDimension = models.IntegerField()
    UnifiedMemory = models.BooleanField()
    AtomicSupport = models.BooleanField()
    HalfPrecisionSupport = models.BooleanField()
    DoubleSupport = models.BooleanField()


