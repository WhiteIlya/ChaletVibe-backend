from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Chalet(models.Model):
    COUNTRY_CHOICES = [
        ('FR', 'France'),
        ('CH', 'Switzerland'),
    ]

    name = models.CharField(max_length=255, verbose_name="Chalet's name")
    image = models.ImageField(upload_to='chalets/', blank=True, null=True, verbose_name="Chalet's picture")
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, default='FR', verbose_name="Country")
    review = models.TextField(blank=True, verbose_name="My opinion")
    chalet_link = models.URLField(verbose_name="Chalet's link")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Chalet's price")
    ski_resort_link = models.URLField(verbose_name="Ski link")
    approximate_travel_time = models.CharField(max_length=100, verbose_name="Approximate time from the airport")
    beds = models.PositiveIntegerField(verbose_name="The amount of beds in the Chalet")

    def __str__(self):
        return self.name


class UserReaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chalet = models.ForeignKey(Chalet, on_delete=models.CASCADE)
    liked = models.BooleanField()

    class Meta:
        unique_together = ('user', 'chalet')

    def __str__(self):
        return f"{self.user} - {self.chalet} - {'Like' if self.liked else 'Dislike'}"