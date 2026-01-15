from django.db import models
from django.contrib.auth.models import User

class PalmTree(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="palms")
    name = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'name'],
                name='unique_palmtree_per_user'
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.owner.username}"

class Diagnosis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="diagnoses")
    palm = models.ForeignKey(PalmTree, on_delete=models.SET_NULL, null=True, blank=True, related_name="diagnoses")
    image = models.ImageField(upload_to="diagnosis/")
    result_label = models.CharField(max_length=100)
    confidence_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)