# django_bootcamp_bank

## Descripción del Proyecto
Este proyecto es una aplicación bancaria desarrollada en Django que permite a los usuarios gestionar sus finanzas de manera eficiente. Los usuarios pueden registrarse, iniciar sesión, realizar depósitos, transferencias y visualizar su historial de transacciones.

## Instrucciones para Ejecutar el Proyecto

### Requisitos Previos
- Python
- PostgreSQL

### Instalación
1. Clona el repositorio:
   ```bash
   git clone https://github.com/protos50/django_bootcamp_bank.git
   cd django_bootcamp_bank
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows usa `venv\\Scripts\\activate`
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura la base de datos PostgreSQL y aplica las migraciones:
   ```bash
   python manage.py migrate
   ```

5. Ejecuta el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

### Configuración de Variables de Entorno
Crea un archivo `.env` en el directorio `src` con el siguiente contenido:
```
DEBUG=True
SECRET_KEY='tu-secreto-aqui'
DB_NAME=name_db
DB_USER=user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

## Funcionalidades Desarrolladas
- Registro e inicio de sesión de usuarios
- Gestión de perfiles de usuario
- Realización de depósitos y transferencias
- Visualización de historial de transacciones
- Gestión de usuarios favoritos
