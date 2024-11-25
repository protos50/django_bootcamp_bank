# django_bootcamp_bank

## Descripción del Proyecto
Este proyecto es una aplicación bancaria desarrollada en Django que permite a los usuarios gestionar sus finanzas de manera eficiente. Los usuarios pueden registrarse, iniciar sesión, realizar depósitos, transferencias y visualizar su historial de transacciones.

## Instrucciones para Ejecutar el Proyecto

### Requisitos Previos
- Python 3.x
- PostgreSQL

### Instalación
1. Clona el repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
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
DATABASE_URL='postgres://usuario:contraseña@localhost:5432/nombre_base_datos'
```

## Funcionalidades Desarrolladas
- Registro e inicio de sesión de usuarios
- Gestión de perfiles de usuario
- Realización de depósitos y transferencias
- Visualización de historial de transacciones
- Gestión de usuarios favoritos