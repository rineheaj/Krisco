from .gallery import gallery_bp
from .upload import upload_bp
from .guestbook import guestbook_bp
from .auth import auth_bp
from .index import index_bp


all_blueprints = [
    gallery_bp,
    upload_bp,
    guestbook_bp,
    auth_bp,
    index_bp,
]