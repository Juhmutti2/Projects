from django.core.management.base import BaseCommand
from datetime import timedelta
from tietokanta.models import Triathlon_Record

class Command(BaseCommand):
    help = 'Add multiple triathlon records'

    def handle(self):
        # Tietue 1
        record1 = Triathlon_Record(
            name="Triathleetti Teemu",
            swim=timedelta(hours=0, minutes=55, seconds=15),
            T1=timedelta(minutes=3, seconds=2),
            cycle=timedelta(hours=5, minutes=45, seconds=30),
            T2=timedelta(minutes=2, seconds=15),
            run=timedelta(hours=4, minutes=20, seconds=45)
        )
        record1.save()
        self.stdout.write(self.style.SUCCESS(f'Record 1 added: Total time: {record1.total}'))

        # Tietue 2
        record2 = Triathlon_Record(
            name="Triathlon Tiina",
            swim=timedelta(hours=1, minutes=30, seconds=45),
            T1=timedelta(minutes=2, seconds=50),
            cycle=timedelta(hours=6, minutes=50, seconds=0),
            T2=timedelta(minutes=8, seconds=30),
            run=timedelta(hours=5, minutes=25, seconds=15)
        )
        record2.save()
        self.stdout.write(self.style.SUCCESS(f'Record 2 added: Total time: {record2.total}'))

        # Lisää lisää tietueita tarpeen mukaan
