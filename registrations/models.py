from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Race(models.Model):
    name = models.CharField(max_length=120)
    date = models.DateField()
    distance_km = models.DecimalField(max_digits=5, decimal_places=2)
    capacity = models.PositiveIntegerField(default=100)
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.name} ({self.distance_km} km)"

class Runner(models.Model):
    GENDER_CHOICES = [('M','Male'),('F','Female'),('O','Other')]
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    age = models.PositiveIntegerField(validators=[MinValueValidator(5), MaxValueValidator(120)], null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"

class Registration(models.Model):
    TSHIRT_CHOICES = [('XS','XS'),('S','S'),('M','M'),('L','L'),('XL','XL'),('XXL','XXL')]
    runner = models.ForeignKey(Runner, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='registrations')
    tshirt_size = models.CharField(max_length=4, choices=TSHIRT_CHOICES, default='M')
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['runner', 'race'], name='unique_runner_race')
        ]

    def __str__(self):
        return f"{self.runner} for {self.race}"
