from django.core.management.base import BaseCommand
from tvmvis.models import Run, Benchmark, TotalResults, TaskGraphResults, TaskResults, SoftwareConfiguration, HardwareConfiguration


class Command(BaseCommand):
    help = 'Deletes all benchmark entries.'

    def handle(self, *args, **options):
        Benchmark.objects.all().delete()
        Run.objects.all().delete()
        TotalResults.objects.all().delete()
        TaskGraphResults.objects.all().delete()
        TaskResults.objects.all().delete()
        SoftwareConfiguration.objects.all().delete()
        HardwareConfiguration.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all tables'))
