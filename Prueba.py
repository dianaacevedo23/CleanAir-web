from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Función para crear la base de datos SQLite y la tabla
def create_db():
    conn = sqlite3.connect('sigfox_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            polvo TEXT,
            gas TEXT,
            carbono TEXT,
            humedad TEXT,
            temperatura TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Ruta principal para mostrar los datos almacenados
@app.route('/')
def index():
    conn = sqlite3.connect('sigfox_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sensor_data ORDER BY timestamp DESC')
    data = cursor.fetchall()
    conn.close()
    return render_template('index.html', data=data)

# Ruta para manejar el callback de Sigfox
@app.route('/sigfox_callback', methods=['POST'])
def sigfox_callback():
    data = request.json
    print("Datos recibidos de Sigfox:", data)

    polvo = data['polvo']['value']
    gas = data['gas']['value']
    carbono = data['carbono']['value']
    humedad = data['humedad']['value']
    temperatura = data['temperatura']['value']

    conn = sqlite3.connect('sigfox_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sensor_data (polvo, gas, carbono, humedad, temperatura)
        VALUES (?, ?, ?, ?, ?)
    ''', (polvo, gas, carbono, humedad, temperatura))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Datos de sensores recibidos y guardados correctamente'}), 200

if __name__ == '__main__':
    create_db()
    app.run(debug=True)
