from .database import db
from sqlalchemy.orm import relationship

class User(db.Model):

    id = db.Column(db.String(80), unique=True, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(100), nullable=False)
    token_rel = relationship("Token", back_populates="user_rel")

class Token(db.Model):

    id = db.Column(db.String(80), unique=True, primary_key=True)
    user_id = db.Column(db.String(80), db.ForeignKey('user.id'))
    user_rel = relationship("User", back_populates="token_rel")

class Invoice(db.Model):

    id = db.Column(db.String(80), unique=True, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    date_sent = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.String(80), db.ForeignKey('user.id'))
    is_incoming = db.Column(db.Boolean, default=True, nullable=False)
    communication_report = relationship("CommunicationReport", back_populates="invoice", uselist=False)
    sent_to_user_id = db.Column(db.String(80), db.ForeignKey('user.id'))

class CommunicationReport(db.Model):

    id = db.Column(db.String(80), unique=True, primary_key=True)
    invoice_id = db.Column(db.String(80), db.ForeignKey('invoice.id'))
    user_id = db.Column(db.String(80), db.ForeignKey('user.id'))
    details = db.Column(db.Text, nullable=False)
    date_reported = db.Column(db.DateTime, nullable=False)
    invoice = relationship("Invoice", back_populates="communication_report")
    user = relationship("User")

# Define relationships after model definitions
User.sent_invoices = relationship('Invoice', foreign_keys=[Invoice.sent_to_user_id], backref="sender")
User.received_invoices = relationship('Invoice', foreign_keys=[Invoice.user_id], backref="receiver")
