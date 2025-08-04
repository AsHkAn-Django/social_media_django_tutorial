from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to="users/%Y/%m/%d", blank=True, null=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('accounts:profile_detail', kwargs={'pk': self.pk})



class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="followings", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="followers", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'user'], name='unique_follow')
        ]

    def clean(self):
        """Check if user is trying to follow himself."""
        if self.follower == self.user:
            raise ValidationError("You can't follow yourself!")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.follower.username} followed {self.user.username}"
