from .database import db
from .models import User, Token, Invoice, CommunicationReport 
def clear():
    db.session.query(User).delete()
    db.session.query(Token).delete()
    db.session.query(Invoice).delete()
    db.session.query(CommunicationReport).delete()
    db.session.commit