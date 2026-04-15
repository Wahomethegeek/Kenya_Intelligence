from django.db import models

class County(models.Model):
    name    = models.CharField(max_length=100)
    slug    = models.SlugField(unique=True)
    code    = models.IntegerField(unique=True) #1-47
    region  = models.CharField(max_length=100) # "Central"


    #Demographics
    population  = models.BigIntegerField(null=True, blank=True)
    area_km2    = models.FloatField(null=True, blank=True)


    #Health
    hospitals   = models.IntegerField(null=True, blank=True)
    health_centres  = models.IntegerField(null=True, blank=True)

    #Education
    primary_schools  = models.IntegerField(null=True, blank=True)
    secondary_schools   = models.IntegerField(null=True, blank=True)

    #Economy
    poverty_index    = models.FloatField(null=True, blank=True) # % below poverty line
    main_activity   = models.CharField(max_length=200, null=True, blank=True)

    #Map
    latitude    = models.FloatField(null=True, blank=True)
    longitude   = models.FloatField(null=True, blank=True)

    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['code']
        verbose_name_plural = "Counties"

    def __str__(self):
        return self.name
