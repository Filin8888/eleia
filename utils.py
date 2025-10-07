import os
from werkzeug.utils import secure_filename
from flask import current_app
import uuid

def save_image(image_file):
    """Зберігає завантажене зображення і повертає його нове ім'я файлу."""
    # Створюємо безпечне ім'я
    filename = secure_filename(image_file.filename)
    # Додаємо унікальний префікс, щоб не перезаписати файли
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    
    # Папка для збереження зображень (налаштуй у config)
    upload_path = os.path.join(current_app.root_path, "static/uploads")
    os.makedirs(upload_path, exist_ok=True)
    
    # Зберігаємо файл
    image_file.save(os.path.join(upload_path, unique_name))
    return unique_name
