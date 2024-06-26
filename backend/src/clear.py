from .database import db
from .models import User, Token, Invoice, CommunicationReport
from flask import Blueprint

clear_ = Blueprint('clear_route', __name__)


# Clears the database
@clear_.route('', methods=['DELETE'])
def clear():
    db.session.query(User).delete()
    db.session.query(Token).delete()
    db.session.query(Invoice).delete()
    db.session.query(CommunicationReport).delete()
    db.session.commit()
    return '', 200
