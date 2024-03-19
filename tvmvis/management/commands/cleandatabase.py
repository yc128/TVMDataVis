from django.core.management.base import BaseCommand
from tvmvis.models import Benchmark


class Command(BaseCommand):
    help = 'Deletes all benchmark entries.'

    def handle(self, *args, **options):
        Benchmark.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all benchmarks'))
