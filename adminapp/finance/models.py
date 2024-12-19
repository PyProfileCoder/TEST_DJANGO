from django.db import models
from django.contrib.auth.models import User

# Expenses Model
class Expenses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to the User model
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.description} - {self.amount}"
