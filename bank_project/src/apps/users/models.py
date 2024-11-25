from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator

class User(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser.
    """
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    balance = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    favorite_users = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='favorited_by',
        blank=True
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'users_user'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.get_full_name() or self.username
