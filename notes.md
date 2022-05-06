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

## Listar las bases de datos

```
\l
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