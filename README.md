# Manual de instalación de la aplicación web

## Decisiones de proyecto

|Elemento|Decisión|Versión|Justificación|
|--------|--------|-------|-------------|
|Servidor web|Apache|2|Sencillo de usar, popular|
|Base de datos|MySQL|8|Experiencia previa, popular|
|Lenguaje servidor|Python|3|Muy interesante para ASIR, uso extendido|
|Framework|Flask|3|Sencillo de usar, pensado especíificamente para web (formularios, sesiones)|
|Control de versiones|Git|2|Muy extendido|
|Documentación|Markdown|-|Muy utilizado con github|

## ¿Qué hace un servidor web?

Recibe peticiones HTTP y devuelve recursos al navegador.

## ¿Qué hace Python?

Es el cerebro de la aplicación web. Tareas que realiza en conjunto con Flask:
- Decidir qué datos pedir a la BD
- Comprobar si un usuario está autenticado
- Validar un formulario
- Calcular cosas
- Insertar/modificar/eliminar datos
- Decidir qué página mostrar
- Devolver respuestas JSON para una API

## ¿Qué es flask?

Framework web ligero para Python que permite crear aplicaciones web mediante rutas y vistas. **Idea clave**: Flask conecta el navegador con la base de datos.

## Proceso de instalación / puesta en marcha

1. Actualizar el sistema
`sudo apt update`
`sudo apt upgrade`
2. Instalar git 
`sudo apt install git`
3. Instalar VSCode + plugins:
    - Markdown all in one
    - Python
4. Instalar apache2
`sudo apt install apache2`
5. Cambiar permisos carpeta /var/www/incidencias.ies.teis
```bash 
sudo chown -R $USER:$USER /var/www/incidencias.ies.teis
sudo chmod -R u=rwX,go=rX /var/www/incidencias.ies.teis
```
6. Instalar mysql server
```bash
sudo apt install mysql-server
```
7. Configuración mysql
```mysql
create database incidencias;
create user 'incidencias'@'localhost' identified by 'incidencias';
grant all privileges on incidencias.* to incidencias'@'localhost';
flush privileges;
create table registros (id int auto_increment primary key, aula varchar(30), usuario varchar(20), descripcion text, estado varchar(25));
insert into registros (aula, usuario, descripcion, estado) values ("Taller1", "ifper
eira", "PC18 no arranca", "Abierta"), ("Taller1", "ifpereira", "Proyector estropeado", "Abierta");
```
8. Instalar Python y componentes relacionados (venv es para crear entornos virtuales y permitir aislar las dependencias Python de este proyecto)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```
9. Crear el entorno virtual y activarlo:
```bash
python3 -m venv venv
source venv/bin/activate
```
10. Instalar flask, conector de bases de datos, comprobar y guardar las dependencias
```bash
pip install flask
pip install mysql-connector-python
pip list
pip freeze > requirements.txt
```
11. Crear gitignore para evitar subir el directorio venv
```gitignore
venv/
__pycache__/
*.pyc
.env
```

## Rutina de trabajo con Flask (venv)

Al empezar:
```bash
cd /var/www/incidencias.ies.teis
source venv/bin/activate
python app.py # Lanzar app
```
Al terminar:
```bash
# ctrl+c parar app
deactivate # salir del entorno
```

## Configuración de git/github

1. Crear repositorio local, añadir archivos y commit
```bash
git init
git add .
git commit -m "comentario"
```
2. Crear cuenta github, crear repositorio en github
3. Conectar repositorio local con remoto
```bash
git remote add origin url-repositorio
git branch -M main
git push -u origin main
```

## Nuestra primera aplicación Python/Flask

1. Creamos un fichero app.py en la carpeta como el siguiente:
```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def inicio():
    return "<h1>Incidencias IES Teis</h1>"


if __name__ == "__main__":
    app.run(debug=True)
```
2. Ejecutamos
```bash
python3 app.py
```
   - Esto crea un servidor web alternativo levantado en localhost en el puerto 5000. Se podría poner Apache de intermediario utilizando un proxy
   - Habría que modificar etc/apache2/sites-available/incidencias.ies.teis.conf añadiendo esto dentro del VirtualHost:
```
    ProxyPass / http://127.0.0.1:5000/
    ProxyPassReverse / http://127.0.0.1:5000/
```
   - Y activar los módulos
```bash
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo systemctl restart apache2
```
3. Comprobamos abriendo http://incidencias.ies.teis:5000

## Migración del formulario a Python/Flask

1. Creamos una carpeta templates y movemos ahí nuestro index.html
2. Modificamos app.py:
```python
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
```
3. Comprobamos abriendo http://incidencias.ies.teis:5000 Hemos conseguido que ahora el formulario lo devuelva Flask

## Recibir los datos del formulario

1. Vamos a app.py y modificamos la primera línea añadiendo request:
```python
from flask import Flask, render_template, request
```
2. Añadimos una ruta en app.py para recibir los datos del formulario:
```python
@app.route("/incidencia", methods=["POST"])
def crear_incidencia():

    aula = request.form["aula"]
    usuario = request.form["usuario"]
    descripcion = request.form["descripcion"]

    print("Aula:" + aula)
    print("Usuario:" + usuario)
    print("Descripción:" + descripcion)

    return "Incidencia recibida"
```
3. Probamos a rellenar el formulario y enviar. Debería pintar en la consola los datos recibidos y mostrar en la página lo que devuelve la función ("Incidencia recibida")

## Introducir los datos en la BD

De momento tenemos los datos en variables de python (aula, usuario y descripcion). Nos falta el paso final de escribir en la BD.

1. 1. Importamos el conector de MySQL después de las importaciones de Flask. El acceso a la base de datos es independiente de Flask:
```python
import mysql.connector
```
2. Añadimos en la función crear_incidencia el código para conectar con la BD e insertar en la tabla (ojo que quede todo bien tabulado y el return al final):
```python
    conexion = mysql.connector.connect(
        host="localhost",
        user="incidencias",
        password="incidencias",
        database="incidencias"
    )

    cursor = conexion.cursor()

    sql = """
        INSERT INTO registros
        (aula, usuario, descripcion, estado)
        VALUES (%s, %s, %s, %s)
    """

    valores = (
        aula,
        usuario,
        descripcion,
        "Abierta"
    )

    cursor.execute(sql, valores)

    conexion.commit()

    cursor.close()
    conexion.close()
```
3. Probamos a enviar el formulario y ver si se inserta una nueva fila en la tabla registros de la BD