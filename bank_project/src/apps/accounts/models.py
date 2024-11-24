from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

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
        db_table = 'accounts_user'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.get_full_name() or self.username

class TransferReason(models.Model):
    """
    Motivos predefinidos para las transferencias.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'transfer_reasons'
        verbose_name = 'Motivo de Transferencia'
        verbose_name_plural = 'Motivos de Transferencia'

    def __str__(self):
        return self.name

class Transaction(models.Model):
    """
    Registro de todas las transacciones (transferencias e ingresos).
    """
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Ingreso de dinero'),
        ('TRANSFER', 'Transferencia'),
    ]

    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    from_user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='sent_transactions'
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='received_transactions',
        null=True,
        blank=True
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    reason = models.ForeignKey(
        TransferReason,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'transactions'
        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'
        ordering = ['-timestamp']

    def __str__(self):
        if self.type == 'DEPOSIT':
            return f"Ingreso de {self.amount} por {self.from_user}"
        return f"Transferencia de {self.amount} de {self.from_user} a {self.to_user}"

    def save(self, *args, **kwargs):
        if self.type == 'TRANSFER':
            # Validar que ambas cuentas estén activas
            if not self.from_user.is_active or not self.to_user.is_active:
                raise ValueError("Las transferencias solo pueden realizarse entre cuentas activas")
            
            # Validar que hay saldo suficiente
            if self.from_user.balance < self.amount:
                raise ValueError("Saldo insuficiente para realizar la transferencia")
            
            # Realizar la transferencia
            self.from_user.balance -= self.amount
            self.to_user.balance += self.amount
            self.from_user.save()
            self.to_user.save()
        
        elif self.type == 'DEPOSIT':
            # Para depósitos, solo actualizamos el balance del usuario
            self.from_user.balance += self.amount
            self.from_user.save()
        
        super().save(*args, **kwargs)
