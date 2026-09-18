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

## Proceso de instalación / puesta en marcha

1. Actualizar el sistema
`sudo apt update`
`sudo apt upgrade`
2. Instalar git 
`sudo apt install git`
3. Instalar VSCode + plugins:
    - Markdown all in one
4. Instalar apache2
`sudo apt install apache2`
5. Cambiar permisos carpeta /var/www/html
```bash 
sudo chown -R $USER:$USER /var/www/html
sudo chmod -R u=rwX,go=rX /var/www/html
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
-- Crear tabla
-- Insertar datos

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

