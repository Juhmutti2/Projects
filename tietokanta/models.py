# Create your models here.

from django.db import models

class Triathlon_Record(models.Model):
    name = models.CharField(max_length=50)  # Nimi, maksimissaan 50 merkkiä
    swim = models.DurationField()  # Uintiaika
    T1 = models.DurationField()  # Ensimmäinen vaihto
    cycle = models.DurationField()  # Pyöräilyaika
    T2 = models.DurationField()  # Toinen vaihto
    run = models.DurationField()  # Juoksuaika

    @property
    def total(self):
        """Laskee kaikkien aikojen summan"""
        return self.swim + self.T1 + self.cycle + self.T2 + self.run

    def __str__(self):
        return self.name
