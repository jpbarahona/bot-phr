# Deploy en Heroku

## Dependencias importantes to Heroku

### gunicorn
Es necesario el archivo Procfile porque permite definir **dynos** (web) que son ligeros contenedores de Linux y que representan a los procesos en la instancia de Heroku, permitiendo levantar correctamente la aplicación

### pipenv
Es un gestor de paquetes como npm en Node o bundle en Ruby, y te permite aislar las dependencias de los proyectos en ambientes independientes con **virtualenv**, facilitando la exportación y su funcionamiento en diferentes instancias. 

Al utilizar pipenv e.g. `pipenv install flask`, genera los archivos Pipfile y Pipfile.lock que son las dependencias del ambiente generado para la aplicación.

## Run Local (development environment)
Es una instancia Flask ejecutada en un ambiente pipenv

Hay que tener instalado:

- Python3 versión: 3.7.3

Clonar repositorio:
```
git clone https://github.com/jpbarahona/bot-phr.git
```

Crear archivo de variables de entorno **.env** en el interior del directorio y agregar:
```
FLASK_ENV=development
```

instalar dependencias de variable
```
pipenv install
```

Ejecutar instancia
```
pipenv run python app.js
```

## Iniciar pipenv

Evitar problemas de `unknown locale: UTF-8` agregar las siguientes lineas por consola

```
export LC_ALL=es_ES.UTF-8
export LANG=es_ES.UTF-8
```
