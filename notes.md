# Installing psycopg2

When we try to install psycopg2 from pip `pip install psycopg2`, an error occurs. In order to solve it, whe must run `pip install psycopg2-binary`. Search in this [site](https://www.psycopg.org/docs/install.html) for more detailes. 

# PostgreSQL

Instalacion.

```
sudo apt-get install postgresql-12
```

Comando para inicializar la base de datos. Postgres por defecto crea el usuario `postgres`.

```
sudo -u postgres psql
```

Comando para instalar un asistente de manejo de las bases de datos de PostgreSQL

```
sudo apt-get install pgadmin3
```

## Listar las bases de datos

```bash
\l
```

## Cambiar base de datos

```bash
\c miniblog
```

## Show tables

```bash
\dt
```

## Ingresar admin user

```bash
INSERT INTO blog_user(name, email, password, is_admin) VALUES ('ADMIN', 'admin@xyz.com', 'pbkdf2:sha256:150000$5oClIM0i$c155be080802a2299bf20f891ea9e542c8fb11ea4a5927d390c36d2d91252a60', TRUE);
```
## Crear un nuevo campo en la tabla posts
```bash
# ALTER TABLE posts ADD COLUMN created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;
Alter table post add column created TIMESTAMP;
```

## Eliminar una base datos por completo
```bash
DROP DATABASE miniblog;
```

## Crea una base de datos
```bash
CREATE DATABASE miniblog;
```


## Crear base de datos

La forma mas simple de hacerlo es:

```
CREATE TABLE <table-name>
```

## Password

Por defecto cuando instalamos postgres, no se crea una contrasenia. Para cambiar dicho comportamiento, podemos crear una, con el siguiente comando.

```
alter user postgres with password <password>
```


# Vocabulario

## Slug: What is a Slug?

A slug is the last part of the url containing a unique string which identifies the resource being served by the web service. In that sense, a slug is a unique identifier for the resource.

## @staticmethod

Este decorador permite que los metodos que definamos en la clase los podamos usar sin necesidad de instanciar la clase.

# Librerias

## Slugify

This library create an _Unique_ slug, which will be usefull to reatrive post later.

```
pip install python-slugify
```
## Flask-migrate

Esta libreria sirve para reconocer los cambios hechos en los modelos de las bases de datos y, asi mismo realizar estas migraciones.

La liberia cuenta con funciones que se ejecutan por *linea de comandos* para realizar las diferentes acciones que deseamos cometer. Entre los diferentes comandos tenemos:

```bash
flask db init
flask db migrate [-m <message>]
flask db upgrade
```

El primero inicia todo el proyecto, es lo mismo que teniamos con el comando `db.create_all()` de SQLAlchemy.
El segundo se encarga de encontrar las modificaciones y crear un nuevo directorio `migrations/` que contendra las migraciones.
Y el tercer es el encargado de ejecutar las migraciones.

Un comando adicional es `flask db migrate -m "Initial database"`, el cual:
>Lo que hace este comando es generar un nuevo fichero con código python que incluye todos los cambios que hay seguir para actualizar la base de datos. Es un fichero de migración y se guarda en el directorio migrations/versions

El anterior comando debe usarse antes de usar `flask db upgrade`

# Creando todas las tablas

Para crear todas las tablas con el asistente de SqlAlchemy, es necesesario crear una base de datos directamente desde postgress. Una vez creada la base de datos, se abre un interprete de python desde la terminal

```bash
python
```

Una vez en el interprete realizamos el siguiente codigo:

```python
from app import db
db.create_all()
```

Y asi se conseguiran crear todas las tablas en cuestion.

References 

1. [Link del tutorial](https://j2logo.com/tutorial-flask-espanol/)

# Creando carpetas y archivos

El siguiente comando crea todas los archivos, incluyendo el directorio `config/`, de configuracion.

En la carpeta de configuracion estan, valga la redundancia, los archivos que se utilizaran en cada escenario al momento de comenzar a desarrollar, testear o mandar a produccion.

*IMPORTANTE:* las carpetas deben estar al **mismo nivel** de `app`

``` bash
cd /home/camiloardilaleg/Desktop/cursos_online/pythonProject/miniblog
mkdir config
cd config
touch  default.py local.py dev.py prod.py staging.py testing.py
cd /home/camiloardilaleg/Desktop/cursos_online/pythonProject/miniblog
```

Ahora la configuracion de `instance/`, en donde se guardan las configuraciones que necesitamos para arrancar el proyecto en *entorno local* y que por tanto, dicha informacion no queremos que se filtre o que otras personas las conozcan.

```
 cd /home/camiloardilaleg/Desktop/cursos_online/pythonProject/miniblog/
 mkdir instance
 cd instance
 touch config.py config-testing.py
 cd /home/camiloardilaleg/Desktop/cursos_online/pythonProject/miniblog
```

Creamos ahora los `templates` para renderizar los errores de manera personalizada

```bash
 cd /home/camiloardilaleg/Desktop/cursos_online/pythonProject/miniblog
 touch app/templates/404.html app/templates/500.html
 echo "abrimos los archivos"
 code app/templates/404.html app/templates/500.html
 echo "cambiamos de nuevo al directorio raiz del proyecto"
 cd /home/camiloardilaleg/Desktop/cursos_online/pythonProject/miniblog
```

Creamos el archivo de decoradores

```bash
 cd /home/camiloardilaleg/Desktop/cursos_online/pythonProject/miniblog
 touch app/auth/decorators.py
 echo "abrimos el archivo"
 code app/auth/decorators.py
```

y anado el siguiente codigo:

```python
from functools import wraps
from flask import abort
from flask_login import current_user

def admin_requires(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        is_admin = getattr(current_user, 'is_admin', False)
        if not is_admin:
            abort(401)
        return func(*args, **kwargs)
    return wrapper
```

Creamos pagina de error personalizada para el error **401**

```bash
 cd /home/camiloardilaleg/Desktop/cursos_online/pythonProject/miniblog
 touch app/templates/401.html
 echo "abrimos el archivo"
 code app/templates/401.html
```

Creamos la plantilla que listará todos los posts
```bash
 cd /home/camiloardilaleg/Desktop/cursos_online/pythonProject/miniblog
 touch app/admin/templates/admin/posts.html
 echo "abrimos el archivo"
 code app/admin/templates/admin/posts.html
```

Creamos la plantilla que listara todos los usuarios
```bash
 cd /home/camiloardilaleg/Desktop/cursos_online/pythonProject/miniblog
 touch app/admin/templates/admin/users.html
 echo "abrimos el archivo"
 code app/admin/templates/admin/users.html
```

creamos la plantilla para mostrar o actualizar un usuario
```bash
 cd /home/camiloardilaleg/Desktop/cursos_online/pythonProject/miniblog
 touch app/admin/templates/admin/user_form.html
 echo "abrimos el archivo"
 code app/admin/templates/admin/user_form.html
```

creamos la pagina principal de admin
```bash
 cd /home/camiloardilaleg/Desktop/cursos_online/pythonProject/miniblog
 touch app/admin/templates/admin/index.html
 echo "abrimos el archivo"
 code app/admin/templates/admin/index.html
```

creamos nuevo formulario para comentarios de invitados
```bash
 touch app/public/forms.py
 code app/public/forms.py
```

```
touch app/common/filters.py


# Testing

El testing, como su nombre lo indica, es una herramienta o una metodologia que nos permite asegurarnos de que nuestro codigo funciona correctamente, sin la necesidad de que un operario exterio testee la pagina manualmente.

**Una ventaja de los test o testing es que, cada vez que modifiquemos el codigo, chequeemos que no hemos dañado nada de nada.**

Primero que hacemos es crear una paquete llamado `tests`

```bash
 cd /home/camiloardilaleg/Desktop/cursos_online/pythonProject/miniblog
 mkdir tests
 cd tests
 echo "Creo el archivo para inicializar el paquete"
 touch __init__.py
 code __init__.py
 touch test_blog_client.py
 echo "abro el archivo"
 code test_blog_client.py
 cd /home/camiloardilaleg/Desktop/cursos_online/pythonProject/miniblog
```

```bash
 cd /home/camiloardilaleg/Desktop/cursos_online/pythonProject/miniblog/
 cd test
 touch test_post_model.py && code test_post_model.py
 cd /home/camiloardilaleg/Desktop/cursos_online/pythonProject/miniblog/
```

## Paginacion o pagination

Se usa cuando el resultado de una consulta es muy grande y no queremos que se muestre todo en una sola pagina. Ademas, de lo costoso computacionalmente que implica dicho proceso. Por tal motivo, se usa la paginacion.



# Enviar mails y servidores SMTP

> Como te decía, para que el objeto Mail pueda enviar mensajes necesita conectarse a un servidor smtp de nuestra propiedad. Para ello, definiremos los siguientes parámetros de configuración en el fichero config/default.py


## Enviar emails de forma asincrona

Creamos un nuevo directorio llamado `common`

```bash
 cd /home/camiloardilaleg/Desktop/cursos_online/pythonProject/miniblog
 mkdir app/common
 cd app/common
 touch __init__.py
 touch mail.py
 code mail.py
 cd /home/camiloardilaleg/Desktop/cursos_online/pythonProject/miniblog
```

# Crear un servidor SMTP

Una manera facil de crear un SMTP es utilizar la libreria `postfix` el cual, con ayuda de un proveedor como gmail permite enviar nuestros emails.

Para dicho cometido se realiza lo siguiente

1. modificamos en el fichero `/etc/hostname` el nombre del servidor a, por ejemplo, `camilo.mail.com`
2. modificamos el fichero `/etc/hosts` y en la linea `127.0.1.1` cambiamos el nombre del servidor a `camilo.mail.com`. asi quedaria
> 127.0.1.1	camilo.mail.com
3. Instalo postfix `apt-get install libsasl2-modules postfix`
4. En el archivo `/etc/postfix/main.cf` cambiamos el nombre del servidor a `camilo.mail.com`. 
quedando de la siguiente manera `myhostname = camilo.mail.com`
5. En google tenemos que generar una contrasena para el servidor smtp.
6. Creamos un arhivo en `/etc/postfix/sasl/sasl_passwd` con el siguiente contenido
>[smtp.gmail.com]:587 camiloardila.publicdiles@gmail.com:<passwd-generado-por-gmail>
7. Encriptamos el archivo y lo colocamos en la base de datos de postfix. Ejecutamos el siguiente comando
`postmap /etc/postfix/sasl/sasl_passwd`
Lo anterior crea un nuevo archivo `sasl_passwd.db`, quedando asi en la carpeta: `/etc/postfix/sasl/sasl_passwd.db`
8. Quitamos prvivilegios al archivo `sasl_passwd` para evitar que las personas que no sean administradores puedan modificarlo o leerlo.
`chown root:root /etc/postfix/sasl/sasl_passwd /etc/postfix/sasl/sasl_passwd` y 
`chmod 0600 /etc/postfix/sasl/sasl_passwd /etc/postfix/sasl/sasl_passwd`
9. En el archivo `/etc/postfix/main.cf' cambiamos la linea `relayhost =` por `relayhost = [smtp.gmail.com]:587`

y al final del mismo archivo anadimos lo siguiente

```
# Enable SASL authentication
smtp_sasl_auth_enable = yes
# Disallow methods that allow anonymous authentication
smtp_sasl_security_options = noanonymous
# Location of sasl_passwd
smtp_sasl_password_maps = hash:/etc/postfix/sasl/sasl_passwd
# Enable STARTTLS encryption
smtp_tls_security_level = encrypt
# Location of CA certificates
smtp_tls_CAfile = /etc/ssl/certs/ca-certificates.crt
```
10. Reiniciamos el servicio postfix
Reiniciamos el servicio postfix con el siguiente comando:
`service postfix restart`

Para enviar correos se procede de la siguiente manera
```
sendmail example@gmail.com
From: root@gmail.com
Subject: Test mail
Testing Email
.
```

Se puede apreciar que se termina con un punto al final.

## Utilizar el servidor SMTP con flask

En el archivo config ponemos la siguiente configuracion

```
# Configuración del email
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'camiloardila.publicfiles@gmail.com'
MAIL_PASSWORD = 'vfwkhwxenmyscmde'
DONT_REPLY_FROM_EMAIL = '(julian, camiloardila.publicfiles@gmail.com)'
ADMINS = ('camiloardila.publicfiles@gmail.com', )
MAIL_USE_TLS = True
MAIL_DEBUG = False
```

# Filters

Los filtros son funciones que permiten modificar el comportamiento al momento de renderizar informacion en las hojas de `jinja`