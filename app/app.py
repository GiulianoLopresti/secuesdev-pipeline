from flask import Flask, request, render_template_string
from markupsafe import escape
import sqlite3
import os

app = Flask(__name__)

@app.after_request
def add_security_headers(response):
    # Corrige: Missing Anti-clickjacking Header
    response.headers['X-Frame-Options'] = 'DENY'
    # Corrige: X-Content-Type-Options Header Missing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    # Corrige: Content Security Policy (CSP) Header Not Set
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    # Corrige: Permissions Policy Header Not Set
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    # Ayuda a mitigar: Server Leaks Version Information
    response.headers['Server'] = 'SecueDevServer'
    return response

# CORRECCION 1: el secreto ya no esta hardcodeado, se lee desde una variable de entorno
API_SECRET_KEY = os.environ.get('API_SECRET_KEY', '')

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

    # CORRECCION 2: SQL Injection corregido usando consulta parametrizada
    # El input del usuario nunca se concatena directo en el string SQL
    conn = get_db_connection()
    query = "SELECT * FROM usuarios WHERE nombre = ?"
    cursor = conn.execute(query, (nombre,))
    resultados = cursor.fetchall()
    conn.close()

    return f"Resultados para: {nombre} -> {resultados}"

@app.route('/saludo')
def saludo():
    # CORRECCION 3: XSS corregido escapando el input antes de insertarlo en HTML
    nombre = request.args.get('nombre', 'invitado')
    nombre_seguro = escape(nombre)
    template = f"<h2>Hola, {nombre_seguro}!</h2>"
    return render_template_string(template)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
