from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# VULNERABILIDAD 1: Secreto hardcodeado en el codigo
API_SECRET_KEY = "sk_live_12345supersecreto"

def get_db_connection():
    conn = sqlite3.connect('usuarios.db')
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, nombre TEXT, email TEXT)')
    conn.execute("INSERT INTO usuarios (nombre, email) SELECT 'admin', 'admin@secuesdev.com' WHERE NOT EXISTS (SELECT 1 FROM usuarios)")
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return '<h1>SecueDev App</h1><p>Bienvenido al sistema de usuarios</p>'

@app.route('/buscar')
def buscar_usuario():
    nombre = request.args.get('nombre', '')

    # VULNERABILIDAD 2: SQL Injection
    # El input del usuario se concatena directo en la query, sin sanitizar
    conn = get_db_connection()
    query = "SELECT * FROM usuarios WHERE nombre = '" + nombre + "'"
    cursor = conn.execute(query)
    resultados = cursor.fetchall()
    conn.close()

    return f"Resultados para: {nombre} -> {resultados}"

@app.route('/saludo')
def saludo():
    # VULNERABILIDAD 3: XSS reflejado
    # El input se inserta directo en el HTML sin escapar
    nombre = request.args.get('nombre', 'invitado')
    template = f"<h2>Hola, {nombre}!</h2>"
    return render_template_string(template)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
