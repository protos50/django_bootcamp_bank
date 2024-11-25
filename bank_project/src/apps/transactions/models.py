from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from apps.users.models import User

class TransferReason(models.Model):
    """
    Motivos predefinidos para las transferencias.
    """
    name = models.CharField('Nombre', max_length=100)
    description = models.TextField('Descripción', blank=True)
    is_active = models.BooleanField('Activo', default=True)
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)

    class Meta:
        verbose_name = 'Motivo de transferencia'
        verbose_name_plural = 'Motivos de transferencia'
        ordering = ['name']

    def __str__(self):
        return self.name

    @classmethod
    def get_default_reason(cls):
        reason, _ = cls.objects.get_or_create(
            name='Otro',
            defaults={'description': 'Motivo por defecto para transferencias'}
        )
        return reason.id

class Transaction(models.Model):
    """
    Registro de todas las transacciones (transferencias e ingresos).
    """
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Ingreso de dinero'),
        ('TRANSFER', 'Transferencia'),
    ]

    type = models.CharField('Tipo', max_length=10, choices=TRANSACTION_TYPES)
    from_user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='sent_transactions',
        verbose_name='Usuario origen'
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='received_transactions',
        verbose_name='Usuario destino'
    )
    amount = models.DecimalField(
        'Monto',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    reason = models.ForeignKey(
        TransferReason,
        on_delete=models.PROTECT,
        verbose_name='Motivo',
        default=TransferReason.get_default_reason
    )
    description = models.TextField('Descripción', blank=True)
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)

    class Meta:
        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_type_display()} - {self.amount} - {self.created_at}"

    def get_amount_for_user(self, user):
        """
        Retorna el monto con el signo correcto según el tipo de transacción y el usuario.
        Para depósitos, siempre es positivo.
        Para transferencias, es negativo si el usuario es from_user, positivo si es to_user.
        """
        if self.type == 'DEPOSIT':
            return self.amount
        elif self.type == 'TRANSFER':
            return -self.amount if self.from_user == user else self.amount
