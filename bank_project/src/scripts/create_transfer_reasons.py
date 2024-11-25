import os
import sys
import django

# Configurar el entorno de Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank_project.settings')
django.setup()

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

def create_transfer_reasons():
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

if __name__ == "__main__":
    create_transfer_reasons()
