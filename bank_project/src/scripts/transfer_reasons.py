from apps.accounts.models import TransferReason

# Lista de razones de transferencia
transfer_reasons = [
    {
        "name": "Alquileres",
        "description": "Pago de alquileres",
    },
    {
        "name": "Aportes de capital",
        "description": "Aportes de capital para negocios",
    },
    {
        "name": "Cuota",
        "description": "Pago de cuotas",
    },
    {
        "name": "Expensas",
        "description": "Pago de expensas",
    },
    {
        "name": "Factura",
        "description": "Pago de facturas",
    },
    {
        "name": "Haberes",
        "description": "Pago de haberes",
    },
    {
        "name": "Honorarios",
        "description": "Pago de honorarios profesionales",
    },
    {
        "name": "Préstamos",
        "description": "Préstamos personales",
    },
    {
        "name": "Seguros",
        "description": "Pago de seguros",
    },
    {
        "name": "Varios",
        "description": "Otros motivos no especificados",
    },
]

print("Creando razones de transferencia...")
for reason in transfer_reasons:
    TransferReason.objects.get_or_create(
        name=reason["name"],
        defaults={
            "description": reason["description"],
            "is_active": True
        }
    )
print("Razones de transferencia creadas exitosamente!")
