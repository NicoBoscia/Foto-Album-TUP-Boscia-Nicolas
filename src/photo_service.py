import os
from werkzeug.utils import secure_filename
from flask import url_for
from .models import Photo
from . import db

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'static/uploads'

def allowed_file(filename: str) -> bool:
    """Verifica si la extensión del archivo es permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_photo(file, title: str, description: str) -> Photo:
    """
    Guarda una nueva foto en la base de datos, con la imagen subida.
    """
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    new_photo = Photo(
        title=title,
        description=description,
        image_url=url_for('static', filename=f'uploads/{filename}')
    )
    db.session.add(new_photo)
    db.session.commit()
    return new_photo
