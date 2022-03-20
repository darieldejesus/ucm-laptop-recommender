# UCM - Laptop Recommender

Sistema de recomendación inteligente desarrollado en Python y utilizando sistema de multi-agentes e inteligencia artificial. Este sistema inteligente busca ofrecer una interfaz donde los usuarios pueden buscar computadoras portátiles (laptops) basado en sus necesidades. Además, ayudar al sistema a mejorar los criterios de recomendación.

## Requisitos

Necesitas tener las siguientes herramientas para la ejecución de este proyecto:

- [Docker](https://docs.docker.com/get-docker/)
- [Python 3](https://www.python.org/downloads/)

## Instalación

Herramientas necesarias para el funcionamiento del sistema:

- **Iniciar Docker**

  Una vez se clone el repositorio de Github, ir al root del proyecto y ejecutar el comando:
  ```sh
  $ docker-compose up -d
  ```
  Este comando se encarga de iniciar los contenedores especificados en el archivo `docker-compose.yml`. En este caso, el servidor XMPP y la base de datos.

- **Configurar XMPP**
  
  Una vez los contenedores esten funcionando, es momento de configurar el usuario administrador en el servidor XMPP para posteriormente agregar los usuarios para cada agente.

  Para acceder al servidor XMPP, solo debemos de ejecutar el comando:
  ```sh
  $ docker exec -it xmpp /bin/sh
  ```
  Donde `xmpp` es el nombre del contenedor que queremos acceder. Una vez dentro, ejecutamos el siguiente comando:
  ```sh
  $ ./bin/ejabberdctl register admin localhost qwerty1234
  ```
  Nota: El usuario `admin` es creado durante la inicialización del servidor XMPP. Acá solo estamos asignando una contraseña a ese usuario, en este caso `qwerty1234`.

  Ahora que completamos el registro del administrador, nos dirigimos al navegador y entramos al apartado del administrador con solo entrar el la dirección http://localhost:5280/admin en el navegador. Solo tienes que introducir el usuario `admin` y la contraseña previamente asignada `qwerty1234`.

- **Agregar usuarios XMPP**
  
  Para la configuración de cada agente, es necesario agregar un usuario con su contraseña. Para esto, vamos a **Dominios Virtuales** > **localhost** > **Usuarios**. Ahí agregamos 4 nuevos usuarios:

  | Usuario | Contraseña |
  |---------|------------|
  | agente1 | qaz123     |
  | agente2 | qaz123     |
  | agente3 | qaz123     |
  | agente4 | qaz123     |

- **Instalar librerias**
  
  Ahora que el servidor XMPP está listo, es momento de instalar las librerias especificadas en `requirements.txt`. Para esto, ejecutamos:
  ```sh
  $ pip install -r requirements.txt
  ```

## Ejecución

Para inicializar el proyecto, es necesario ejecutar el comando para inicializar los contenedores de Docker y ejecutar el script de Python.

- Preparar los contenedores de Docker:
  ```sh
  $ docker-compose up -d
  ```
- Ejecutar el comando de Python:
  ```sh
  $ python start.py
  ```
  Para deneter la ejecución, solo es necesario introducir la combinación de teclado `Ctrl + C`.
