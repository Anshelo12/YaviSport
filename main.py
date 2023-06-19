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


#RETURN "INDEX"
@app.route('/')
def index():
    return render_template('login.html')
#RETURN "ENTREGA"
@app.route('/entrega')
def entrega():
    return render_template('entrega.html')
#RETURN "NOSOTROS"
@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')
#RETURN "PARA REGALAR"
@app.route('/pararegalar')
def pararegalar():
    return render_template('pararegalar.html')
#RETURN "TRATAMIENTO"
@app.route('/tratamiento')
def tratamiento():
    return render_template('tratamiento.html')
#RETURN "DECORATIVAS"
@app.route('/decorativas')
def decorativas():
    return render_template('decorativas.html')
#RETURN "AROMATICAS"
@app.route('/aromaticas')
def aromaticas():
    return render_template('aromaticas.html')
#RETURN "SERVICIOS"
@app.route('/servicios')
def servicios():
    return render_template('servicios.html')
#RETURN "CONTACTANOS"
@app.route('/contactanos')
def contactanos():
    return render_template('contactanos.html')

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
                return redirect(url_for('products'))
            else:
                
                flash('Usuario no Existe')
        else:
            
            flash('Usuario  no Existe')
 
    return render_template('login.html')

#register
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
    return render_template('register.html')
 
@app.route('/add', methods=['POST'])
def add_product_to_cart():
    _quantity = int(request.form['quantity'])
    _code = request.form['code']
    # validate the received values
    if _quantity and _code and request.method == 'POST':
 
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
        cursor.execute('SELECT * FROM product WHERE code = %s', (_code,))
        row = cursor.fetchone()
                 
        itemArray = { row['code'] : {'name' : row['name'], 'code' : row['code'], 'quantity' : _quantity, 'price' : row['price'], 'image' : row['image'], 'total_price': _quantity * row['price']}}
                 
        all_total_price = 0
        all_total_quantity = 0
                 
        session.modified = True
        if 'cart_item' in session:
            if row['code'] in session['cart_item']:
                for key, value in session['cart_item'].items():
                    if row['code'] == key:
                        old_quantity = session['cart_item'][key]['quantity']
                        total_quantity = old_quantity + _quantity
                        session['cart_item'][key]['quantity'] = total_quantity
                        session['cart_item'][key]['total_price'] = total_quantity * row['price']
            else:
                session['cart_item'] = array_merge(session['cart_item'], itemArray)
         
            for key, value in session['cart_item'].items():
                individual_quantity = int(session['cart_item'][key]['quantity'])
                individual_price = float(session['cart_item'][key]['total_price'])
                all_total_quantity = all_total_quantity + individual_quantity
                all_total_price = all_total_price + individual_price
        else:
            session['cart_item'] = itemArray
            all_total_quantity = all_total_quantity + _quantity
            all_total_price = all_total_price + _quantity * row['price']
             
        session['all_total_quantity'] = all_total_quantity
        session['all_total_price'] = all_total_price
                 
        return redirect(url_for('products'))
    else:
        return 'Error while adding item to cart'
 
@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('.products'))
    except Exception as e:
        print(e)
 
@app.route('/delete/<string:code>')
def delete_product(code):
    try:
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True
         
        for item in session['cart_item'].items():
            if item[0] == code:    
                session['cart_item'].pop(item[0], None)
                if 'cart_item' in session:
                    for key, value in session['cart_item'].items():
                        individual_quantity = int(session['cart_item'][key]['quantity'])
                        individual_price = float(session['cart_item'][key]['total_price'])
                        all_total_quantity = all_total_quantity + individual_quantity
                        all_total_price = all_total_price + individual_price
                break
         
        if all_total_quantity == 0:
            session.clear()
        else:
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price
             
        return redirect(url_for('.carrito'))
    except Exception as e:
        print(e)
 
def array_merge( first_array , second_array ):
    if isinstance( first_array , list ) and isinstance( second_array , list ):
        return first_array + second_array
    elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
        return dict( list( first_array.items() ) + list( second_array.items() ) )
    elif isinstance( first_array , set ) and isinstance( second_array , set ):
        return first_array.union( second_array )
    return False
 
if __name__ == "__main__":
    app.run(debug=True)
#fin carrito




@app.route('/redirecciona')
def redirecciona(sitio=None):
    if sitio is not None:
        return redirect(url_for('index'))
    else:
        return redirect(url_for('acercade'))

# Con parametros
def pagina_no_encontrada(error):
    return render_template('errores/404.html'), 404


if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.secret_key = 'clave-flask'
    app.run(debug=True, port=5000)






