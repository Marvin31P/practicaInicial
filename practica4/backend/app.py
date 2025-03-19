from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Clave secreta para la sesión

login_manager = LoginManager()
login_manager.init_app(app)

# Simulamos una base de datos de usuarios en memoria
users = {}

# Simulamos una base de datos de publicaciones en memoria
publicaciones = []

# Clase para manejar el usuario
class User(UserMixin):
    def __init__(self, username):
        self.id = username

# Cargar un usuario por ID
@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Vista de login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users.get(username)
        if user and user['password'] == password:
            login_user(User(username))
            return redirect(url_for('home'))
        flash('Credenciales incorrectas', 'error')
        return redirect(url_for('login'))

    return render_template('accounts/login.html')

@app.route('/home')
@login_required
def home():
    """Página de inicio"""
    return render_template('home.html')

@app.route('/profile')
@login_required
def profile():
    """Página de perfil del usuario"""
    user_data = users[current_user.id]
    return render_template('profile.html', user=user_data)

@app.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    logout_user()
    return redirect(url_for('login'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Vista para registrar un nuevo usuario"""
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        email = request.form['email']
        nombre = request.form['nombre']
        carnet = request.form['carnet']
        
        if password1 != password2:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(url_for('registro'))

        if username in users:
            flash('El nombre de usuario ya existe', 'error')
            return redirect(url_for('registro'))

        users[username] = {
            'password': password1,
            'email': email,
            'nombre': nombre,
            'carnet': carnet
        }

        flash(f'Cuenta creada para {username}!', 'success')
        return redirect(url_for('login'))

    return render_template('accounts/registro.html')

### 🔹 **NUEVO ENDPOINT: CREAR PUBLICACIÓN**
@app.route('/publicacion', methods=['POST'])
@login_required
def crear_publicacion():
    """Permite a los usuarios autenticados crear publicaciones"""
    data = request.json  # Recibe datos en formato JSON
    
    if not data or 'titulo' not in data or 'contenido' not in data:
        return jsonify({'error': 'Faltan datos'}), 400

    nueva_publicacion = {
        'usuario': current_user.id,
        'titulo': data['titulo'],
        'contenido': data['contenido']
    }

    publicaciones.append(nueva_publicacion)

    return jsonify({'mensaje': 'Publicación creada exitosamente', 'publicacion': nueva_publicacion}), 201

### 🔹 **NUEVO ENDPOINT: LISTAR PUBLICACIONES**
@app.route('/publicaciones', methods=['GET'])
def listar_publicaciones():
    """Devuelve todas las publicaciones registradas"""
    return jsonify(publicaciones)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
