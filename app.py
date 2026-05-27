from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from models import db, Product, User
import os

load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('MYSQL_PUBLIC_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def home():

    products = Product.query.filter_by(active=True).all()

    return render_template(
        'index.html',
        products=products
    )


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():

    error = None

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(
            username=username,
            active=True
        ).first()

        if user and user.check_password(password):

            session['admin'] = True
            session['user_id'] = user.id
            session['username'] = user.username

            return redirect(url_for('dashboard'))

        error = 'Usuario o contraseña incorrectos'

    return render_template(
        'login.html',
        error=error
    )


@app.route('/admin/dashboard')
def dashboard():

    if not session.get('admin'):

        return redirect(url_for('admin_login'))

    products = Product.query.all()

    return render_template(
        'dashboard.html',
        products=products
    )


@app.route('/admin/create-product', methods=['GET', 'POST'])
def create_product():

    if not session.get('admin'):

        return redirect(url_for('admin_login'))

    error = None

    if request.method == 'POST':

        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        image = request.files.get('image')

        if not name or len(name) < 3 or len(name) > 80:

            error = 'El nombre debe tener entre 3 y 80 caracteres'

            return render_template(
                'create_product.html',
                error=error
            )
        try:
            price = float(price)

            if price <= 0:
                error = 'El precio debe ser mayor a 0'
                return render_template('create_product.html', error=error)

            if price > 99999999:
                error = 'El precio no puede ser mayor a 99.999.999'
                return render_template('create_product.html', error=error)

        except:
            error = 'Precio inválido'
            return render_template('create_product.html', error=error)

        if not image or image.filename == '':

            error = 'Debes subir una imagen'

            return render_template(
                'create_product.html',
                error=error
            )

        allowed_extensions = (
            '.png',
            '.jpg',
            '.jpeg',
            '.webp'
        )

        if not image.filename.lower().endswith(allowed_extensions):

            error = 'Formato de imagen no permitido'

            return render_template(
                'create_product.html',
                error=error
            )

        filename = secure_filename(image.filename)

        image.save(
            os.path.join(
                app.config['UPLOAD_FOLDER'],
                filename
            )
        )

        product = Product(
            name=name,
            description=description,
            price=price,
            image=f'/static/uploads/{filename}'
        )

        db.session.add(product)
        db.session.commit()

        return redirect(url_for('dashboard'))

    return render_template(
        'create_product.html',
        error=error
    )


@app.route('/admin/edit-product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):

    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    product = Product.query.get_or_404(id)
    error = None

    if request.method == 'POST':

        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        image = request.files.get('image')

        if not name or len(name) < 3 or len(name) > 80:
            error = 'El nombre debe tener entre 3 y 80 caracteres'
            return render_template('edit_product.html', product=product, error=error)

        try:
            price = int(price)

            if price <= 0:
                error = 'El precio debe ser mayor a 0'
                return render_template('edit_product.html', product=product, error=error)

            if price > 99999999:
                error = 'El precio no puede ser mayor a 99.999.999'
                return render_template('edit_product.html', product=product, error=error)

        except:
            error = 'Precio inválido'
            return render_template('edit_product.html', product=product, error=error)

        product.name = name
        product.description = description
        product.price = price

        if image and image.filename != '':

            allowed_extensions = ('.png', '.jpg', '.jpeg', '.webp')

            if not image.filename.lower().endswith(allowed_extensions):
                error = 'Formato de imagen no permitido'
                return render_template('edit_product.html', product=product, error=error)

            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    filename
                )
            )

            product.image = f'/static/uploads/{filename}'

        db.session.commit()

        return redirect(url_for('dashboard'))

    return render_template(
        'edit_product.html',
        product=product,
        error=error
    )


@app.route('/admin/delete-product/<int:id>')
def delete_product(id):

    if not session.get('admin'):

        return redirect(url_for('admin_login'))

    product = Product.query.get_or_404(id)

    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('dashboard'))


@app.route('/admin/users')
def users():

    if not session.get('admin'):

        return redirect(url_for('admin_login'))

    users = User.query.all()

    return render_template(
        'users.html',
        users=users
    )


@app.route('/admin/create-user', methods=['GET', 'POST'])
def create_user():

    if not session.get('admin'):

        return redirect(url_for('admin_login'))

    error = None

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:

            error = 'Ese usuario ya existe'

            return render_template(
                'create_user.html',
                error=error
            )

        if not username or len(username) < 3:

            error = 'El usuario debe tener mínimo 3 caracteres'

            return render_template(
                'create_user.html',
                error=error
            )

        if not password or len(password) < 6:

            error = 'La contraseña debe tener mínimo 6 caracteres'

            return render_template(
                'create_user.html',
                error=error
            )

        user = User(
            username=username,
            role='admin',
            active=True
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('users'))

    return render_template(
        'create_user.html',
        error=error
    )


@app.route('/admin/delete-user/<int:id>')
def delete_user(id):

    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    current_user = User.query.get(session.get('user_id'))

    if not current_user or current_user.username != 'admin':
        return redirect(url_for('users'))

    user = User.query.get_or_404(id)

    if user.username == 'admin':
        return redirect(url_for('users'))

    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('users'))


@app.route('/admin/logout')
def logout():

    session.clear()

    return redirect(url_for('home'))


with app.app_context():

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.create_all()

    admin = User.query.filter_by(username='admin').first()

    if not admin:

        admin = User(
            username='admin',
            role='admin',
            active=True
        )

        admin.set_password('123456')

        db.session.add(admin)
        db.session.commit()


if __name__ == '__main__':

    app.run(debug=True)