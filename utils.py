from werkzeug.utils import secure_filename
import os
from datetime import datetime

def save_image(image_file):
    """Save uploaded image and return filename"""
    if not image_file:
        return None
    
    filename = secure_filename(image_file.filename)
    unique_filename = f"{datetime.now().timestamp()}_{filename}"
    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
    image_file.save(image_path)
    return unique_filename