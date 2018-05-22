# Deploy en Heroku

## Dependencias importantes

### gunicorn
Es necesario el archivo Procfile porque permite definir ** dynos ** (web) que son ligerons contenedores de Linux y que representan a los procesos en la instancia de Heroku, permitiendo levantar correctamente la aplicación

### pipenv
Es un gestor de paquetes como npm en Node o bundle en Ruby, y te permite aislar las dependencias de los proyectos en ambientes independientes con **virtualenv**, facilitando la exportación y su funcionamiento en diferentes instancias. 

Al utilizar pipenv e.g. `pipenv install flask`, genera los archivos Pipfile y Pipfile.lock que son las dependencias del ambiente generado para la aplicación.

## Run Local

```
git clone https://github.com/jpbarahona/bot-phr.git
pipenv install
pipenv run python app.js
```