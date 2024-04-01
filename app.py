from flask import Flask, render_template_string
import requests

app = Flask(__name__)
@app.route('/character/<id>')
def character_details(id):
    # Realizar la solicitud a la API para obtener los detalles del personaje por ID
    response = requests.get(f'https://dragonball-api.com/api/characters/{id}')
    data = response.json()

    # Plantilla HTML para los detalles del personaje
    html_template = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Detalles del Personaje</title>
        <style>
            table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
            }
            th, td {
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
            img {
                width: 100px;
                height: auto;
            }
        </style>
    </head>
    <body>
    <h2>Información del Personaje</h2>
    <table>
        <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Ki</th>
            <th>Max Ki</th>
            <th>Raza</th>
            <th>Género</th>
            <th>Descripción</th>
            <th>Imagen</th>
            <th>Afiliación</th>
            <th>Planeta de Origen</th>
        </tr>
        <tr>
            <td>{{ data['id'] }}</td>
            <td>{{ data['name'] }}</td>
            <td>{{ data['ki'] }}</td>
            <td>{{ data['maxKi'] }}</td>
            <td>{{ data['race'] }}</td>
            <td>{{ data['gender'] }}</td>
            <td>{{ data['description'] }}</td>
            <td><img src="{{ data['image'] }}" alt="Imagen de {{ data['name'] }}"></td>
            <td>{{ data['affiliation'] }}</td>
            <td>{{ data['originPlanet']['name'] if data.get('originPlanet') else 'Desconocido' }}</td>
        </tr>
    </table>
    """

    # Añade la sección de transformaciones si existen
    if 'transformations' in data and data['transformations']:
        html_template += """
        <h2>Transformaciones</h2>
        <table>
            <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Imagen</th>
                <th>Ki</th>
            </tr>
            {% for transformation in data['transformations'] %}
            <tr>
                <td>{{ transformation['id'] }}</td>
                <td>{{ transformation['name'] }}</td>
                <td><img src="{{ transformation['image'] }}" alt="Imagen de {{ transformation['name'] }}"></td>
                <td>{{ transformation['ki'] }}</td>
            </tr>
            {% endfor %}
        </table>
        """
    
    html_template += "</body></html>"

    # Renderiza la plantilla HTML con los datos del personaje
    return render_template_string(html_template, data=data)

@app.route('/')
def home():
    api_url = 'https://dragonball-api.com/api/characters?limit=1000'
    response = requests.get(api_url)
    data = response.json()

    html_template = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dragon Ball Characters</title>
        <style>
            table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
            }
            th, td {
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
            img {
                width: 100px;
                height: auto;
            }
            body{
                margin-left: 20px;
            }
        </style>
    </head>
    <body>
    <table>
        <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Ki</th>
            <th>Max Ki</th>
            <th>Raza</th>
            <th>Genero</th>
            <th>Descripcion</th>
            <th>Imagen</th>
            <th>Afiliacion</th>
            <th>Detalles</th>
        </tr>
        {% for item in items %}
        <tr>
            <td>{{ item['id'] }}</td>
            <td>{{ item['name'] }}</td>
            <td>{{ item['ki'] }}</td>
            <td>{{ item['maxKi'] }}</td>
            <td>{{ item['race'] }}</td>
            <td>{{ item['gender'] }}</td>
            <td>{{ item['description'] }}</td>
            <td><img src="{{ item['image'] }}" alt="{{ item['name'] }}" style="width: 100px; height: auto;"></td>
            <td>{{ item['affiliation'] }}</td>
            <td><a href="/character/{{ item['id'] }}">Ver detalles</a></td>
        </tr>
        {% endfor %}
    </table>
    </body>
    </html>
    """
    
    return render_template_string(html_template, items=data.get('items', []))

if __name__ == '__main__':
    app.run(debug=True)
