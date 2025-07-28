from django.db import models
from django.conf import settings

# Create your models here.

class GameResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    number = models.IntegerField()
    result = models.CharField(max_length=10, choices=[
        ('win', 'Win'),
        ('lose', 'Lose'),
    ])
    prize = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.number} - {self.result}"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['result', 'created_at']),
            models.Index(fields=['created_at']),
        ]
