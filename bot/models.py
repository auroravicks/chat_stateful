from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Messages(models.Model):
    sender_types={
        'User': 'User',
        'Agent': 'Agent',
        'System': 'System'
    }
    sender = models.CharField(
        max_length=6,
        choices=sender_types,
        default='User'
    )
    #is_user = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender}: {self.content}'