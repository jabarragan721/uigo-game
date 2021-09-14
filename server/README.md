# uigo-game server

Se recomienda usar Python 3.9

## Usar un entorno virtual

Un entorno virtual ayuda a separar las dependencias de este proyecto y evita mezclarse con otros


**Crear el entorno virtual**

Es una convención utilizar *env* como nombre del entorno pero se puede utilizar otro nombre

```
python3 -m venv env
```

**Activar el entorno creado**

Si en el anterior paso se creó el entorno con un nombre diferente, se tiene que cambiar *env* aqui también

```
source env/bin/activate
```

Para desactivar el entorno usar `deactivate`

**Instalar las dependencias**

La instalación de las dependencias se debe hacer con el entorno activo, de lo contrario se instalarán de forma global

```
pip install -r ./requirements.txt
```

## Iniciar el server

```
python3 server.py
```