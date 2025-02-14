from django.db import models


class Place(models.Model):
    class Meta:
        verbose_name = 'Місце'
        verbose_name_plural = 'Місця'

    def __str__(self):
        return self.name

    name = models.CharField(verbose_name='назва', max_length=255)
