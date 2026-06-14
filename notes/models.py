from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    NOTE_TYPES = (
        ("note", "Note"),
        ("todo", "Todo"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    type = models.CharField(max_length=10, choices=NOTE_TYPES, default="note")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TodoItem(models.Model):
    note = models.ForeignKey(
        Note, on_delete=models.CASCADE, related_name="items")
    text = models.CharField(max_length=255)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.text
