# apicultur-examples
Ejemplos utilizando la API de Apicultur


## Requisitos
Tienes que tener Python y `pip` instalados

## Ejecutar los ejemplos
 1. Instalar la librería de apicultur:

    ```python
    pip install apicultur
    ```
    
 2. Descargarte este repositorio (puedes clonarlo con Git o hacer [download](https://github.com/Lingwars/apicultur-examples/archive/master.zip))
 3. Consigue un `access_token` en Apicultur
 4. Crea un archivo `secret.py` con el siguiente contenido:

    ```python
    ACCESS_TOKEN = 'aquí-va-el-access_token'
    ```
    
 5. Ahora ya puedes ejecutar los ejemplos
 
    ```bash
    python contar_lemas.py data/100words.txt
    ```

¿Has creado algún ejemplo interesante que quieres compartir? ¡Mándanos un pull-request!
