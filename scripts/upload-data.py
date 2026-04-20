import json
import os
import psycopg2

# 1. Configuración de la base de datos (Asegurarse que coincida con el docker-compose)
DB_HOST = "localhost"
DB_NAME = "bleach_db"
DB_USER = "user"
DB_PASS = "password"

def connect_db():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    return conn

def load_json_files(directory):
    # Lista para guardar todos los personajes
    all_characters = []

    # Recorremos la carpeta donde guardamos los json
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # NOTA: depende de si la lista es una lista [] o un objeto {}
                # Si el archivo tiene una lista de personajes, extendemos nuestra lista
                if isinstance(data, list):
                    all_characters.extend(data)
                else:
                    all_characters.append(data)
    return all_characters

def insert_characters(conn, characters):
    cursor = conn.cursor()

    query = """
    INSERT INTO characters (name, race, gender, affiliation, rank, image_url)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    for char in characters:
        # Acá viene la limpieza de datos
        # Mapeamos las llaves del JSON a las columnas de la tabla
        # Usamos el método .get() para evitar errores por si falta un dato en el JSON

        name = char.get('name', 'unknown')
        race = char.get('race', 'Unknown') # O quizás viene del nombre del archivo?
        gender = char.get('gender', 'Unknown')
        affiliation = char.get('affiliation', 'None')
        rank = char.get('rank', 'None')
        image = char.get('image', '')

        cursor.execute(query, (name, race, gender, affiliation, rank, image))

    conn.commit()
    cursor.close()
    print(f"Se han insertado {len(characters)} personajes")

# Ejecución
if __name__ == "__main__":
    try:
        conn = connect_db()
        # Asumiendo que los json están en una carpeta llamada 'characters_data'
        personajes = load_json_files('./characters_data')
        insert_characters(conn, personajes)
    except Exception as e:
        print(f"Ocurrió un error: {e}")