from django.db import models

# Create your models here.
class Province(models.Model):


    alias = models.CharField(max_length=20)
    province = models.CharField(max_length=50, verbose_name='province')

    def __str__(self):
        return ' | '.join([self.alias, self.province])


class City(models.Model):


    class Meta:
        verbose_name_plural = 'Cities/Municipalities'
    

    city_class_choices = [
        (1, 'cc'),
        (2, 'huc'),
        (3, 'icc'),
        (4, 'municipality'),
    ]

    alias = models.CharField(max_length=5)
    city = models.CharField(max_length=50, verbose_name='city/municipality')
    city_class = models.IntegerField(choices=city_class_choices)
    province = models.ForeignKey(Province)

    def __str__(self):
        return ' | '.join([self.alias, self.city])