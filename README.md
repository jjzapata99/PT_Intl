### Prueba Técnica Jose Zapata

- En el repositorio se encontrarán dos carpetas según lo solicitado.
- Con la finalidad de un despliegue rapido se creo un docker-compose.yml.
- Si se desea ejecutar individualmente se lo puede hacer a traves del nombre de cada servicio, api_fastapi y api_express respectivamente.
- En cada archivo existen comentarios que intentan explicar la funcionalidad de cada bloque de codigo.


Caracteristicas Generales
-------------
Ambos proyectos cuentan con sus archivos .gitignore, .dockerignore, .env que por motivos de seguridad se adjunta el archivo .env_example.
Para la ejecución en local para cada proyecto es necesario la instalacion del requirements y package.json según corresponda. Ademas del uso de los siguientes comandos:

FastAPI:
- uvicorn main:app --reload --env-file=.env

Express:
- npm run dev

FastAPI
-------------
Se genero un API Rest para la obtención de un url de pagos por medio de paypal, para esto se uso las librerias de [paypal for developers](https://developer.paypal.com/home "paypal for developers"),  y para el manejo de los tokens y seguridad, las librerias de JWT y FastAPI.

Express
-------------
Se genero un API Rest el cual realiza la firma de un archivo pdf a partir de un certificado .p12, esta API cuenta con un apartado visual en [ip]:[port]/home, con la finalidad de hacer la carga y descarga del archivo de una forma más sencilla, haciendo uso de las librerias de [signPDF](https://github.com/vbuch/node-signpdf "signPDF"), asi mismo se hace uso de tokens para el manejo de la seguridad y haciendo uso de las librerias de JWT.

Nota: Asegurese de tener creado las carpetas uploads y signed dentro de intelnexts, ya que en estas carpetas se guardaran los archivos subidos y firmados.

