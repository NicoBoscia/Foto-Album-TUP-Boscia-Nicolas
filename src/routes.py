import os
from flask import Blueprint, render_template, request, redirect, url_for, Response
from . import db
from typing import List, Union
from .models import Photo
from .forms import PhotoForm
from werkzeug.utils import secure_filename

photo_bp = Blueprint('photo_bp', __name__)

# Configuración para la carga de archivos
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')

# Función para verificar si el archivo tiene una extensión válida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Página principal que muestra todas las fotos
@photo_bp.route("/")
def index() -> str:
    """
    Ruta principal que muestra todas las fotos.
    """
    photos: List[Photo] = Photo.query.all()  # Tipamos la variable 'photos' como una lista de objetos Photo
    return render_template('index.html', photos=photos)

# Página para agregar nuevas fotos
@photo_bp.route("/new", methods=["GET", "POST"])
def new_photo() -> Union[str, Response]:
    """
    Ruta para crear una nueva foto.
    Retorna un HTML si es GET o una redirección si es POST.
    """
    form = PhotoForm()
    if form.validate_on_submit():
        if 'image_url' not in request.files:
            return redirect(request.url)
        file = request.files['image_url']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            new_photo = Photo(
                title=form.title.data,
                description=form.description.data,
                image_url=url_for('static', filename=f'uploads/{filename}')
            )
            db.session.add(new_photo)
            db.session.commit()
            return redirect(url_for('photo_bp.index'))
    return render_template('photo_form.html', form=form)

@photo_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_photo(id):
    photo = Photo.query.get_or_404(id)  # Obtener la foto por su id
    form = PhotoForm(obj=photo)  # Pre-llenamos el formulario con los datos existentes

    if form.validate_on_submit():
        photo.title = form.title.data
        photo.description = form.description.data

        # Si se ha subido una nueva imagen
        if 'image_url' in request.files:
            file = request.files['image_url']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                photo.image_url = url_for('static', filename=f'uploads/{filename}')

        db.session.commit()
        return redirect(url_for('photo_bp.index'))
    
    return render_template('photo_form.html', form=form, photo=photo)

@photo_bp.route("/delete/<int:id>")
def delete_photo(id):
    photo = Photo.query.get_or_404(id)
    db.session.delete(photo)
    db.session.commit()
    return redirect(url_for('photo_bp.index'))


