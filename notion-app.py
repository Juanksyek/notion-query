import requests

# Tu clave de API de Notion
notion_api_key = 'secret_dn2OAPSqDRTYJ3SoIfJKEQQ37JkbUTKjwGmzoFbk4He'
notion_database_id = 'f8828d071c9349a596a6a4f66e3fd5b6'

# Claves de API de OMDb y Google Books
omdb_api_key = '9589a21b'  # Solo la clave, sin la URL completa
google_books_api_key = 'tu_google_books_api_key'  # Reemplaza con tu clave

# Función para obtener información de películas y series
def get_movie_info(title):
    url = f'http://www.omdbapi.com/?t={title}&apikey={omdb_api_key}'
    response = requests.get(url)
    return response.json()

# Función para obtener información de libros
def get_book_info(title):
    url = f'https://www.googleapis.com/books/v1/volumes?q={title}&key={google_books_api_key}'
    response = requests.get(url)
    data = response.json()
    if 'items' in data:
        return data['items'][0]['volumeInfo']
    else:
        return None

# Función para agregar entrada a Notion
def add_to_notion(title, info, type_):
    headers = {
        'Authorization': f'Bearer {notion_api_key}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28'
    }
    url = 'https://api.notion.com/v1/pages'

    if type_ == 'movie':
        properties = {
            'Title': {'title': [{'text': {'content': title}}]},
            'Director': {'rich_text': [{'text': {'content': info.get('Director', 'Desconocido')}}]},
            'Year': {'number': int(info.get('Year', 0))},
            'Genre': {'rich_text': [{'text': {'content': info.get('Genre', 'Desconocido')}}]},
            'Platform': {'rich_text': [{'text': {'content': 'Desconocido'}}]},
        }
    elif type_ == 'book' and info is not None:
        properties = {
            'Title': {'title': [{'text': {'content': title}}]},
            'Author': {'rich_text': [{'text': {'content': ', '.join(info.get('authors', ['Desconocido']))}}]},
            'Published Date': {'date': {'start': info.get('publishedDate', 'Desconocido')}},
            'Genre': {'rich_text': [{'text': {'content': ', '.join(info.get('categories', ['Desconocido']))}}]},
            'Platform': {'rich_text': [{'text': {'content': 'Desconocido'}}]},
        }
    else:
        return {'error': 'No information found for the given title'}

    data = {
        'parent': {'database_id': notion_database_id},
        'properties': properties
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Ejemplo de uso
# title = "The Matrix"
# movie_info = get_movie_info(title)
# add_to_notion(title, movie_info, 'movie')

title = "Hunger Games"
book_info = get_book_info(title)
if book_info is not None:
    add_to_notion(title, book_info, 'book')
else:
    print(f"No se encontró información para el libro '{title}'")
