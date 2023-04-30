from django.db import models
from users.models import User


# Create your models here.


class Article(models.Model):
    class Meta:
        db_table = "Todolist"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completion_at = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self):
        return str(self.title)
