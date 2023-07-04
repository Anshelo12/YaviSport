from flask import Flask, redirect, url_for, render_template, request, flash, session, jsonify
import psycopg2
import psycopg2.extras
import re 
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key='yavisport'
host =     'localhost'
database = 'YaviSport'
username = 'postgres'
password = 'anshe12'
port =      5432
 
conn = psycopg2.connect(host=host, database=database,
                   user=username, password=password, port=port)


#RETURN "INICIO"
@app.route('/')
def inicio():
    return render_template('inicio.html')
#RETURN "ADMIN"
@app.route('/admin')
def admin():
    return render_template('admin.html')
#RETURN "INSCRITOS"
@app.route('/inscritos')
def inscritos():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM inscripcione")
    datos = cursor.fetchall()
    cursor.close()
    return render_template('inscritos.html', datos=datos)
#RETURN "PROGRAMACION"
@app.route('/programacion')
def programacion():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM programacionp")
    datos = cursor.fetchall()
    cursor.close()
    return render_template('programacion.html', datos=datos)
#RETURN "PARTIDOS JUGADOSS"
@app.route('/jugados')
def jugados():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM partidosju")
    datos = cursor.fetchall()
    cursor.close()
    return render_template('jugados.html', datos=datos)
#RETURN "POSICION"
@app.route('/posiciones')
def posiciones():
    return render_template('posiciones.html')

#login
@app.route('/login/', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
   
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print(password) 
       
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))       
        account = cursor.fetchone() 
        if account:
            password_rs = account['password']
            print(password_rs)           
            if check_password_hash(password_rs, password):                
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']               
                return redirect(url_for('admin'))
            else:
                
                flash('Usuario no Existe')
        else:
            
            flash('Usuario  no Existe')
 
    return render_template('login.html')

#register
def validar_nombre(fullname):
    if fullname[0].isupper() and fullname.isalpha():
        return True
    return False

def validar_correo(email):
    if "@" in email:
        return True
    return False

def validar_usuario(username):
    if len(username) >= 4 and any(char.isdigit() for char in username):
        return True
    return False

def validar_contrasena(password):
    if 8 <= len(password) <= 16 and any(char.isalpha() for char in password) and any(char.isdigit() for char in password):
        return True
    return False

@app.route('/register', methods=['GET', 'POST'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']    
        _hashed_password = generate_password_hash(password)
       
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        print(account)       
        if account:
            flash('la cuenta ya existe!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Correo Invalido!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('El nombre de usuario debe contener solo caracteres y números!')
        elif not username or not password or not email:
            flash('Por favor rellena el formulario!')
        else:           
            cursor.execute("INSERT INTO users (fullname, username, password, email) VALUES (%s,%s,%s,%s)", (fullname, username, _hashed_password, email))
            conn.commit()
            return render_template('login.html')
    elif request.method == 'POST':       
        flash('Por favor llena los campos del registro!')  
        
        if validar_nombre(fullname) and validar_correo(email) and validar_usuario(username) and validar_contrasena(password):
            
            return "Registro exitoso"
        else:
            return "Error en el registro. Verifica los campos e inténtalo nuevamente." 
    return render_template('register.html')

#registro inscripcion
@app.route('/inscripcion',  methods=['GET', 'POST'])
def inscripcion():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        idins = request.form.get('idins')  # Obtener el ID del formulario de edición si existe
        numeroe = request.form['numeroe']
        nombree = request.form['nombree']
        nombred = request.form['nombred']
        telefono = request.form['telefono']
        Categoriae = request.form['Categoriae']

        if idins:  # Si hay un ID, es una solicitud de edición
            cursor.execute("UPDATE inscripcione SET numeroe = %s, nombree = %s, nombred = %s, telefono = %s, Categoriae = %s WHERE idins = %s", (numeroe, nombree, nombred, telefono, Categoriae, idins))
        else:  # Si no hay un ID, es una solicitud de creación
            cursor.execute("INSERT INTO inscripcione (numeroe, nombree, nombred, telefono, Categoriae) VALUES (%s, %s, %s, %s, %s)", (numeroe, nombree, nombred, telefono, Categoriae))
        conn.commit()

    cursor.execute("SELECT * FROM inscripcione")
    datos = cursor.fetchall()
    cursor.close()

    return render_template('inscripcion.html', datos=datos)
@app.route('/editarins/<int:idins>', methods=['GET', 'POST'])
def editarins(idins):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST':
        numeroe = request.form['numeroe']
        nombree = request.form['nombree']
        nombred = request.form['nombred']
        telefono = request.form['telefono']
        Categoriae = request.form['Categoriae']

        cursor.execute("UPDATE inscripcione SET numeroe = %s, nombree = %s, nombred = %s, telefono = %s, Categoriae = %s WHERE idins = %s", (numeroe, nombree, nombred, telefono, Categoriae, idins))
        conn.commit()

        return redirect(url_for('inscripcion'))

    cursor.execute("SELECT * FROM inscripcione WHERE idins = %s", (idins,))
    dato = cursor.fetchone()
    cursor.close()

    return render_template('inscripcion.html', dato=dato)
@app.route('/borrarins/<int:idins>', methods=['GET', 'POST'])
def borrarins(idins):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST':
        # Eliminar el registro de la base de datos
        cursor.execute("DELETE FROM inscripcione WHERE idins = %s", (idins,))
        conn.commit()

    # Obtener los datos actualizados de la tabla
    cursor.execute("SELECT * FROM inscripcione")
    datos = cursor.fetchall()
    cursor.close()

    return render_template('inscripcion.html', datos=datos)

#registro programacion partidos
@app.route('/partidospro',  methods=['GET', 'POST'])
def partidospro():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        idp = request.form.get('idp')  # Obtener el ID del formulario de edición si existe
        equipo1pro = request.form['equipo1pro']
        equipo2pro = request.form['equipo2pro']
        fechapro = request.form['fechapro']
        estadiopro = request.form['estadiopro']

        if idp:  # Si hay un ID, es una solicitud de edición
            cursor.execute("UPDATE programacionp SET equipo1pro = %s, equipo2pro = %s, fechapro = %s, estadiopro = %s WHERE idp = %s", (equipo1pro, equipo2pro, fechapro, estadiopro, idp))
        else:  # Si no hay un ID, es una solicitud de creación
            cursor.execute("INSERT INTO programacionp (equipo1pro, equipo2pro, fechapro, estadiopro) VALUES (%s, %s, %s, %s, %s)", (equipo1pro, equipo2pro, fechapro, estadiopro))
        conn.commit()
    cursor.execute("SELECT * FROM programacionp")
    datos = cursor.fetchall()
    cursor.close()

    return render_template('partidospro.html', datos=datos)
@app.route('/editarpar/<int:idp>', methods=['GET', 'POST'])
def editarpar(idp):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST':
        equipo1pro = request.form['equipo1pro']
        equipo2pro = request.form['equipo2pro']
        fechapro = request.form['fechapro']
        estadiopro = request.form['estadiopro']

        cursor.execute("UPDATE programacionp SET equipo1pro = %s, equipo2pro = %s, fechapro = %s, estadiopro = %s WHERE idp = %s", (equipo1pro, equipo2pro, fechapro, estadiopro, idp))
        conn.commit()

        return redirect(url_for('partidospro'))
    cursor.execute("SELECT * FROM programacionp WHERE idp = %s", (idp,))
    dato = cursor.fetchone()
    cursor.close()

    return render_template('partidospro.html', dato=dato)
@app.route('/borrarpar/<int:idp>', methods=['GET', 'POST'])
def borrarpar(idp):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST':
        # Eliminar el registro de la base de datos
        cursor.execute("DELETE FROM programacionp WHERE idp = %s", (idp,))
        conn.commit()

    # Obtener los datos actualizados de la tabla
    cursor.execute("SELECT * FROM programacionp")
    datos = cursor.fetchall()
    cursor.close()

    return render_template('partidospro.html', datos=datos)

#registro partidos jugados
@app.route('/partidosju',  methods=['GET', 'POST'])
def partidosju():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        idj = request.form.get('idj')  # Obtener el ID del formulario de edición si existe
        equipo1jug = request.form['equipo1jug']
        equipo2jug = request.form['equipo2jug']
        equipogana = request.form['equipogana']

        if idj:  # Si hay un ID, es una solicitud de edición
            cursor.execute("UPDATE partidosju SET equipo1jug = %s, equipo2jug = %s, equipogana = %s WHERE idj = %s", (equipo1jug, equipo2jug, equipogana, idj))
        else:  # Si no hay un ID, es una solicitud de creación
            cursor.execute("INSERT INTO partidosju (equipo1jug, equipo2jug, equipogana) VALUES (%s, %s, %s)", (equipo1jug, equipo2jug, equipogana))
        conn.commit()

    cursor.execute("SELECT * FROM partidosju")
    datos = cursor.fetchall()
    cursor.close()

    return render_template('partidosju.html', datos=datos)
@app.route('/editarju/<int:idj>', methods=['GET', 'POST'])
def editarju(idj):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST':
        equipo1jug = request.form['equipo1jug']
        equipo2jug = request.form['equipo2jug']
        equipogana = request.form['equipogana']

        cursor.execute("UPDATE partidosju SET equipo1jug = %s, equipo2jug = %s, equipogana = %s WHERE idj = %s", (equipo1jug, equipo2jug, equipogana, idj))
        conn.commit()

        return redirect(url_for('partidosju'))

    cursor.execute("SELECT * FROM partidosju WHERE idj = %s", (idj,))
    dato = cursor.fetchone()
    cursor.close()

    return render_template('partidosju.html', dato=dato)
@app.route('/borrarju/<int:idj>', methods=['GET', 'POST'])
def borrarju(idj):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST':
        # Eliminar el registro de la base de datos
        cursor.execute("DELETE FROM partidosju WHERE idj = %s", (idj,))
        conn.commit()

    # Obtener los datos actualizados de la tabla
    cursor.execute("SELECT * FROM partidosju")
    datos = cursor.fetchall()
    cursor.close()

    return render_template('partidosju.html', datos=datos)




#registro tabla de posiciones
@app.route('/tablap',  methods=['GET', 'POST'])
def tablap():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        equipo1pro = request.form['equipo1pro']
        equipo2pro = request.form['equipo2pro']
        fechapro = request.form['fechapro']
        estadiopro = request.form['estadiopro']

        # Realizar la inserción en la base de datos
        cursor.execute("INSERT INTO programacionp (equipo1pro, equipo2pro, fechapro, estadiopro) VALUES (%s, %s, %s, %s)", (equipo1pro, equipo2pro, fechapro, estadiopro))
        conn.commit()

        cursor.close()

        return 'Datos guardados exitosamente'
    return render_template('tablap.html')
 
@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('.products'))
    except Exception as e:
        print(e)

# Con parametros
def pagina_no_encontrada(error):
    return render_template('errores/404.html'), 404


if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.secret_key = 'clave-flask'
    app.run(debug=True, port=5000)






