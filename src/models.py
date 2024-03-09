from .database import db
from sqlalchemy.orm import relationship
# from flask_login import UserMixIn

class User(db.Model):
    id = db.Column(db.String(80), unique=True, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    #token = db.Column(db.String(150), unique=True, nullable=True)
    token_rel = relationship("Token", back_populates="user")


class Token(db.Model):
    id = db.Column(db.String(80), unique=True, primary_key=True)
    user_id = db.Column(db.String(80), db.ForeignKey('user.id'))
    user = relationship("User", back_populates="token_rel")


class Invoice(db.Model):
    id = db.Column(db.String(80), unique=True, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.String(255), nullable=False) #Maybe change db.string to db.text
    date_sent = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.String(80), db.ForeignKey('user.id')) # Foreign key when receiving.
    is_incoming = db.Column(db.Boolean, default=True, nullable=False)
    communication_report = relationship("CommunicationReport", back_populates="invoice", uselist=False)
    sent_to_user_id = db.Column(db.String(80), db.ForeignKey('user.id')) # Foreign key when sending.


class CommunicationReport(db.Model):
    id = db.Column(db.String(80), unique=True, primary_key=True)
    invoice_id = db.Column(db.String(80), db.ForeignKey('invoice.id'))
    details = db.Column(db.Text, nullable=False)
    date_reported = db.Column(db.DateTime, nullable=False)
    invoice = relationship("Invoice", back_populates="communication_report")

User.sent_invoices = relationship('Invoice', foreign_keys=[Invoice.sent_to_user_id])
User.received_invoices = relationship('Invoice', foreign_keys=[Invoice.user_id])