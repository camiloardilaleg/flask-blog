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

```
\l
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

# Librerias

## Slugify

This library create an _Unique_ slug, which will be usefull to reatrive post later.

```
pip install python-slugify
```

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

Creamos ahora los `templtes` para renderizar los errores de manera personalizada

```bash
 cd /home/camiloardilaleg/Desktop/cursos_online/pythonProject/miniblog
 touch app/templates/404.html app/templates/500.html
 echo "abrimos los archivos"
 code app/templates/404.html app/templates/500.html
 echo "cambiamos de nuevo al directorio raiz del proyecto"
 cd /home/camiloardilaleg/Desktop/cursos_online/pythonProject/miniblog
```
