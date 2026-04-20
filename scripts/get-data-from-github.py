import requests
import os

def descargar_archivos_json():
    """ 
    Consult the GitHub API to obtain the list of files in the 'data' folder
    and download those with the .json extension.
    
    The process is:
    1. GET to the GitHub API.
    2. Filter by type 'file' and extension '.json'.
    3. Download the raw content and save it locally.
    
    Raises:
        requests.exceptions.RequestException: If there is a network error.
    """
    # Configuración del repositorio
    usuario = "ashishk1331"
    repositorio = "bleach-database"
    carpeta = "data"

    # Carpeta donde la almacenaremos los archivos
    carpeta_destino = "characters_data"
    os.makedirs(carpeta_destino, exist_ok=True)

    # 1. URL de la API de GitHub para leer el contenido de la carpeta
    url_api = f"https://api.github.com/repos/{usuario}/{repositorio}/contents/{carpeta}"

    print(f"Consultando archivos en: {url_api}")
    respuesta = requests.get(url_api)

    if respuesta.status_code == 200:
        archivos = respuesta.json()

        # 2. Iterar sobre la lista de archivos
        for archivo in archivos:
            nombre = archivo['name']

            # 3. Filtrar archivos que solo terminan en .json
            if nombre.endswith('.json') and archivo['type'] == 'file':
                url_descarga = archivo['download_url']
                print(f"Descargando {nombre}...")

                # 4. Descargar el contenido crudo (aparentemente esa vaina tiene nombre, se llama 'craw' de un archivo)
                contenido = requests.get(url_descarga).content

                # 5. Guardar archivo en disco o ssd (en el almacenamiento pues)
                ruta_final = os.path.join(carpeta_destino, nombre) # No te voy a mentir, acá le pedí ayuda a gemini porque no me acordaba de los métodos para esta vaina
                with open(ruta_final, 'wb') as f:
                    f.write(contenido)

        print(f"\nTodos los archivos .json se han guardado en la carpeta '{carpeta_destino}'.")
    
    elif respuesta.status_code == 404:
        print("Error: No se encontró el repositorio o la carpeta. Verifica que la URL sea correcta.")
    else:
        print(f"Error: al conectar con Github. Código de estado: {respuesta.status_code}")

if __name__ == "__main__":
    descargar_archivos_json()