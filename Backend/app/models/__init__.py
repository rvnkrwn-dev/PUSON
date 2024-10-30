from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .puskesmas import Puskesmas
from .posyandu import Posyandu
from .anak import Anak
from .pemeriksaan import Pemeriksaan
from .stunting import Stunting
from .refresh_token import RefreshToken
from .log import Log
