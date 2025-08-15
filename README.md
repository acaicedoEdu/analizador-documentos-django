# Analizador de Documentos (Proyecto Django)

Este es un proyecto desarrollado con Django y Django Rest Framework para analizar documentos.

## 🚀 Instalación y Ejecución

Sigue estos pasos para levantar el proyecto en un entorno de desarrollo local.

### **1. Prerrequisitos**

* Python 3.8 o superior
* Pip (manejador de paquetes de Python)
* Git

### **2. Clonar el Repositorio**

```bash
git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
cd tu-repositorio/
```

### **3. Configurar el Entorno Virtual**

```bash
# Crear el entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# En macOS/Linux:
source venv/bin/activate
```

### **4. Instalar Dependencias**

Instala todas las librerías necesarias que se encuentran en el archivo `requirements.txt`.

```bash
pip install -r requirements.txt
```

### **5. Aplicar Migraciones de la Base de Datos**

Este comando creará la base de datos (SQLite por defecto) y las tablas necesarias para el proyecto.

```bash
python manage.py migrate
```

### **6. Ejecutar el Servidor de Desarrollo**

¡Ya está todo listo! Inicia el servidor de Django.

```bash
python manage.py runserver
```

El servidor estará corriendo en `http://127.0.0.1:8000/`.