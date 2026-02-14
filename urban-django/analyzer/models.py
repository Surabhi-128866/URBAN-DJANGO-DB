from django.db import models

class Habitat(models.Model):
    name = models.CharField(max_length=100)
    population_density = models.IntegerField(help_text="People per sq km")
    crime_rate = models.FloatField(help_text="Crime index (lower is better)")
    green_space = models.FloatField(help_text="Percentage of green area")
    schools = models.IntegerField(default=0)
    hospitals = models.IntegerField(default=0)
    restaurants = models.IntegerField(default=0)
    malls = models.IntegerField(default=0)
    description = models.TextField()
    image_url = models.URLField(max_length=500, blank=True, null=True)
    
    # New fields for Map and Advanced Analysis
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    pollution_level = models.IntegerField(default=50) # 0-100 (0=Clean, 100=Heavily Polluted)
    
    # User Association
    from django.contrib.auth.models import User
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('name', 'user')

    def __str__(self):
        return self.name
