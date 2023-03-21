# Scraper de Inmuebles :house:

> Me quiero mudar

Este proyecto busca inmuebles en algunas páginas con los filtros que quieras y manda un bonito mensaje de telegram a un grupo con los inmuebles nuevos que encuentra en esas páginas.

### Páginas Habilitadas :white_check_mark:

- [Zonaprop](https://www.zonaprop.com.ar/)
- [Argenprop](https://www.argenprop.com/)
- [Mercadolibre](https://www.mercadolibre.com.ar)
- [Clasificados La Voz](https://clasificados.lavoz.com.ar/inmuebles)
- [Properati](https://www.properati.com.ar/)

## Instalación :wrench:

### Requerimientos Previos :nut_and_bolt:

1. Saber lo que es una terminal/consola y poder manejarte entre carpetas en una.

2. Vas a necesitar tener instalado Python. Si no lo tenés instalado, [acá te dejo un link](https://tutorial.djangogirls.org/es/python_installation/)

3. Clonar este repo. Si no sabés clonar un repositorio, [acá te dejo un link](https://www.taloselectronics.com/blogs/tutoriales/como-descargar-un-proyecto-de-github)

### Setup :hammer:

1. Abrir una terminal/consola<s>/tostadora</s> donde puedas usar python.

2. Ir a la carpeta del repositorio en tu computadora.

2. Crear un entorno virtual y activarlo corriendo lo siguiente:

```bash
python -m venv venv
source venv/bin/activate
```

3. Instalar lo que necesita el comando para funcionar:

```bash
pip install -r requirements.txt
```

4. Listop, ahora podes empezar a configurar el script!

## Configuración :pencil:

### Bot de Telegram :envelope:

1. Para poder utilizar este proyecto tenés vas a tener que crearte un bot, agregarlo a un grupo. Nosotros vamos a utilizar el token del bot y el "Chat ID" del grupo. Si no sabes cómo conseguir esas cosas [acá te dejo un link](https://dev.to/rizkyrajitha/get-notifications-with-telegram-bot-537l). 

2. No pierdas estas cosas, las vamos a necesitar en el futuro.

### Links de Búsqueda :mag:

Es necesario decirle al script los filtros que vos pones cuando buscas inmuebles y lo vamos a hacer pasandole el link generado por las páginas cuando agregas los filtros a la búsqueda.

1. Buscá en las páginas habilitadas que desees con los filtros que queres y andá a la segunda página de la búsqueda. (Zona, si es casa o depto, dormitorios, lo que quieras)

2. Copiá el link que te sale cuando haces esa busqueda, pegalo en algún lado y fijate que al final puede decir algo cómo `-pagina-2.html` borrá el número de página y pone `{}`. El link se debería terminar con algo así `-pagina-{}.html`, `-pagina-{}` o `&page={}` (no está implementada la paginación para mercadolibre así que no es necesario hacer esto último para ese link).

3. No pierdas estas cosas, las vamos a necesitar en el futuro.

### Archivo de Configuración :page_facing_up:

1. Creá un archivo dentro de la carpeta del repositorio que se llame `config.yaml` que se vea más o menos así:

```yaml
persist: true # En `true` hace que el script no pare
sleep_time: 3 # Hace que el script se ejecute cada 3 segundos
bot_token: "1234567899:asdasdsadasdasdsaddgZ5RAguDlq67dA" # Token de bot
chat_room: "-1801651256762" # id de chat
pages: 5 # Cantidad de páginas que ver por link
zonaprop_full_url: "https://www.zonaprop.com.ar/loquesea-pagina-{}.html" # busqueda zonaprop
mercadolibre_full_url: "https://inmuebles.mercadolibre.com.ar/departamentos/alquiler/loquesea" # busqueda mercadolibre
argenprop_full_url: "https://www.argenprop.com/loquesea-pagina-{}" # busqueda argenprop
la_voz_full_url: "https://clasificados.lavoz.com.ar/inmuebles/loquesea&page={}" # busqueda la voz
properati_full_url: "https://www.properati.com.ar/s/departamento/alquiler/loquesea&page={}" # busqueda properati
```

Donde:

- `persist` _(opcional, default: `false`)_: Hace que el script se ejecute sin parar. Si es configurado en `false` va a hacer la busqueda una sola vez, en `true` busca nuevos departamentos permanentemente.
- `sleep_time` _(opcional, default: `5`)_: Tiempo que espera antes de hacer la busqueda nuevamente en segundos.
- `bot_token`: Token del bot de telegram.
- `chat_room`: id del chat en donde el bot envía los mensajes.
- `pages` _(opcional, default: `3`)_: Cantidad de páginas en las que querés que vea en tu búsqueda en zonaprop/argenprop.
- `pagina_full_url` _(opcional)_: URL del link en el que buscar.

2. Profit.

## Uso :rainbow:

1. Abrir una terminal

2. Ir a la carpeta del repositorio

3. Activar el entorno virtual:

```bash
source venv/bin/activate
```

4. Correr el script pasándole el archivo de configuración

```bash
python main.py ./config.yaml
```

Listo! :tada: Ahora te deberían empezar a llegar mensajes desde tu bot.

## Agradecimientos :pray:

Muchas gracias a [fernandezpablo85](https://gist.github.com/fernandezpablo85) porque [este articulo](https://dev.to/fernandezpablo/scrappeando-propiedades-con-python-4cp8) es el que dió origen a este proyecto y ayudó a que pueda encontrar una casa.
