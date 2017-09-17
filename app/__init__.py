from .app import ThreadApp
from .tasks import Tasks

flask_app = ThreadApp()

from app import views
