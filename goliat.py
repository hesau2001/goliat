from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
from flask_bcrypt import bcrypt
from PIL import Image
import base64


goliatApp = Flask(__name__)
goliatApp.config['MYSQL_HOST'] = 'localhost'
goliatApp.config['MYSQL_USER'] = 'root'
goliatApp.config['MYSQL_PASSWORD'] = 'mysql'
goliatApp.config['MYSQL_DB'] = 'goliat'
goliatApp.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(goliatApp)

idUsuarioG = ""


def saveIdUsuario(idUsuarioLogin):
    global idUsuarioG
    idUsuarioG = str(idUsuarioLogin)
    


@goliatApp.route('/')
def index():
    return render_template("login.html")


@goliatApp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        nombres = request.form['nombresUsua']
        apellidos = request.form['apellidosUsua']
        fechaNacimiento = request.form['fechaNaciUsua']
        numeroCel = request.form['numeroCelUsua']
        trabajo = request.form['trabajoUsua']
        tituloUniversitario = request.form['gradoUniUsua']
        pais = request.form['paisOrigenUsua']
        estado = request.form['estadoOrigenUsua']
        ciudad = request.form['ciudadOrigenUsua']
        usuario = request.form['usuario']
        email = request.form['emailUsua']
        clave = request.form['contraUsua'].encode('utf-8')
        claveConfirm = request.form['contraUsua1'].encode('utf-8')
        if clave == claveConfirm:
            claveCifrada = bcrypt.hashpw(clave, bcrypt.gensalt())
            empleados = mysql.connection.cursor()
            empleados.execute("INSERT INTO usuario (nombresUsua, apellidosUsua, fechaNaciUsua, numeroCelUsua, trabajoUsua, gradoUniUsua, paisOrigenUsua, estadoOrigenUsua, ciudadOrigenUsua,  usuario, emailUsua, contraUsua) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                              (nombres.upper(), apellidos.upper(), fechaNacimiento, numeroCel, trabajo, tituloUniversitario, pais, estado, ciudad, usuario, email,  claveCifrada,))
            mysql.connection.commit()
            empleados.close()
            return redirect(url_for('login'))
        else:
            return 'Contraseña incorrecta'


@goliatApp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['contraUsua'].encode('utf-8')
        selUsuario = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        selUsuario.execute(
            "SELECT * FROM usuario WHERE usuario = %s", (usuario,))
        u = selUsuario.fetchone()
        selUsuario.close()
        if u is not None:
            if bcrypt.hashpw(clave, u["contraUsua"].encode('utf-8')) == u["contraUsua"].encode('utf-8'):
                session["nombresUsua"] = u["nombresUsua"]
                saveIdUsuario(u["idUsuario"])
                return render_template('home.html')
            else:
                return 'Error: clave incorrecta'
        else:
            return 'Error: usuario no existe'
    else:
        return render_template("login.html")


@goliatApp.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')


@goliatApp.route('/home')
def home():
    return render_template('home.html')


@goliatApp.route('/uploadPerfil')
def perfil():
    return render_template('uploadPerfil.html')

@goliatApp.route('/uploadImagen', methods=["POST"])
def uploadImagen():
    imagenCamino = request.form["imagenUsuario"]
    with open(r"C:\Server\me.jpg", 'rb') as imagen:
        informacionBinaria = imagen.read()
    
    insertImagen = mysql.connection.cursor()
    insertImagen.execute("INSERT INTO prueba (imagen) VALUES (%s)", (informacionBinaria,))
    mysql.connection.commit()
    insertImagen.execute("SELECT * FROM  prueba")
    img =  insertImagen.fetchall()
    insertImagen.close
    return render_template('uploadPerfil.html', imagenes = img)




@goliatApp.route('/actividades')
def actividades():
    return render_template('actividades.html')

# - - - - -  - - - - - - - - - - - - - - - - Perfil- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
#------------------------------------------- Selecion del Perfil ------------------------------------------------#
@goliatApp.route('/sPerfil', methods=["POST", "GET"])
def sPerfil():
    selUsuario = mysql.connection.cursor()
    selUsuario.execute(
        "SELECT * FROM usuario WHERE idUsuario = %s", (idUsuarioG,))
    usuario = selUsuario.fetchone()
    selUsuario.close()
    return render_template('perfil.html', perfil=usuario)


@goliatApp.route('/iPerfil', methods=["POST"])
def iPerfil():
    nombres = request.form['nombresUsua']
    apellidos = request.form['apellidosUsua']
    fechaNacimiento = request.form['fechaNaciUsua']
    trabajo = request.form['trabajoUsua']
    tituloUniversitario = request.form['gradoUniUsua']
    pais = request.form['paisOrigenUsua']
    estado = request.form['estadoOrigenUsua']
    ciudad = request.form['ciudadOrigenUsua']
    usuario = request.form['usuario']
    email = request.form['emailUsua']
    clave = request.form['contraUsua'].encode('utf-8')
    claveCifrada = bcrypt.hashpw(clave, bcrypt.gensalt())
    empleado = mysql.connection.cursor()
    empleado.execute("INSERT INTO usuario (nombresUsua, apellidosUsua, fechaNaciUsua,  trabajoUsua, gradoUniUsua, paisOrigenUsua, estadoOrigenUsua, ciudadOrigenUsua,  usuario, emailUsua, contraUsua) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                     (nombres.upper(), apellidos.upper(), fechaNacimiento, trabajo, tituloUniversitario, pais, estado, ciudad, usuario, email, claveCifrada,))
    mysql.connection.commit()
    empleado.close()
    return redirect(url_for('sPerfil'))


@goliatApp.route('/uPerfil', methods=["POST"])
def uPerfil():
    idUsuario = request.form['idUsuario']
    nombres = request.form['nombresUsua']
    apellidos = request.form['apellidosUsua']
    fechaNacimiento = request.form['fechaNaciUsua']
    trabajo = request.form['trabajoUsua']
    celular = request.form['numeroCelUsua']
    tituloUniversitario = request.form['gradoUniUsua']
    pais = request.form['paisOrigenUsua']
    estado = request.form['estadoOrigenUsua']
    ciudad = request.form['ciudadOrigenUsua']
    usuario = request.form['usuario']
    email = request.form['emailUsua']
    clave = request.form['contraUsua'].encode('utf-8')
    claveCifrada = bcrypt.hashpw(clave, bcrypt.gensalt())
    empleado = mysql.connection.cursor()
    empleado.execute("UPDATE usuario SET nombresUsua = %s, apellidosUsua = %s, fechaNaciUsua = %s,  trabajoUsua = %s, numeroCelUsua = %s, gradoUniUsua = %s, paisOrigenUsua = %s, estadoOrigenUsua = %s, ciudadOrigenUsua = %s,  usuario = %s, emailUsua = %s, contraUsua= %s WHERE idUsuario = %s",
                     (nombres.upper(), apellidos.upper(), fechaNacimiento, trabajo, celular, tituloUniversitario, pais, estado, ciudad, usuario, email, claveCifrada, idUsuario))
    mysql.connection.commit()
    empleado.close()
    return redirect(url_for('sPerfil'))


@goliatApp.route('/dPerfil', methods=['POST'])
def dPerfil():
    delUsuario = mysql.connection.cursor()
    delUsuario.execute("DELETE FROM usuario WHERE idUsuario = %s", (idUsuarioG,))
    mysql.connection.commit()
    delUsuario.close()
    return redirect(url_for('logout'))


if __name__ == '__main__':
    goliatApp.secret_key = 'goliatGana'
    goliatApp.run(port=3000, debug=True)
