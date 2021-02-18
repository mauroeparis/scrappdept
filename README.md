# Scrapper de Inmuebles

> Me quiero mudar

Este proyecto busca inmuebles con los filtros que quieras y manda un mensaje de telegram a un grupo con los inmuebles nuevos que encuentra.

Hasta el día 18/02/2012 solo están implementados los conectores de Zonaprop, Argenprop y Mercado Libre.

> El de mercado libre anda medio mal pero anda y hay un intento de implementar el de Olx pero encontramos una casa antes de terminarlo bien.

Sentite libre de abrir PRs, forkear, abrir issues, seguirme en twitter que tengo twitter y seguirme en instagram que tengo instagram.

## Instrucciones

### Configurar donde buscar

1. Primero buscá en Zonaprop, Mercado Libre y/o Argenprop con los filtros que queres. (Zona, si es casa o depto, dormitorios, lo que quieras)

2. Copiá el link que te sale cuando haces esa busqueda y pegalo dentro del archivo correspondiente dentro de la carpeta `connectors` en la variable `full_url` o `_full_url` según corresponda. Fijate que en el que está al final puede decir `-pagina-{}.html` borrá la parte de `.html` de tu link poné eso al final para poder buscar dentro de varias páginas.

3. Configurá la cantidad de páginas que queres que vea el scrapper con la variable `number_of_pages` dentro del mismo archivo.

> En mercadolibre.py esta variable no está.

### Configurar Bot de Telegram

1. Para poder utilizar este proyecto tenés vas a tener que crearte un bot y agregarlo a un grupo. Nosotros vamos a utilizar el token del bot y el "Chat ID" del grupo. Si no sabes cómo conseguir esas cosas [acá te dejo un link](https://dev.to/rizkyrajitha/get-notifications-with-telegram-bot-537l). 

2. Una vez que tenés esas cosas, vas a clonar este repo e ir a la carpeta en donde lo pongas. Si no sabés clonar un repositorio [acá te dejo un link](https://www.taloselectronics.com/blogs/tutoriales/como-descargar-un-proyecto-de-github)

3. Ahora vas a ir al archivo `connectors/base.py` y poner el token de tu bot dentro de la variable `bot_token` y el id del chat en la variable `chat_room`. Te debería quedar algo asi: 
```python
# Telegram bot token here
bot_token = "23523523525:DSOIGUHEODGHGdasdsadSADSD4"
# Chat roop ID goes here
chat_room = "-32523532532"
```

> Puede que tu token y el chat id se vean distintos a los que puse ahi.

### Correr programa

1. Para poder correr esto vas a necesitar Python. Si no lo tenés instalado, nuevamente [acá te dejo un link](https://tutorial.djangogirls.org/es/python_installation/)

22. Bien, finalmente vas a correr lo siguiente en una terminal dentro de la carpeta del repo:

```bash
python main.py
```

Ahora te deberían empezar a llegar mensajes desde tu bot.

## Agradecimientos

Muchas gracias a [fernandezpablo85](https://gist.github.com/fernandezpablo85) porque [este articulo](https://dev.to/fernandezpablo/scrappeando-propiedades-con-python-4cp8) es el que dió origen a este proyecto y ayudó a que pueda encontrar una casa.
