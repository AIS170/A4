from .database import db
from .models import User
def clear():
    with db.session() as session:
        data_clear = session.query(User).filter_by(User.first_name).all()
        
        for data in data_clear:
            session.delete(data)
            
        session.commit()
    
clear()