from hashlib import md5
from app import app


ROLE_USER = 0
ROLE_ADMIN = 1



class User():
    id = 1
    nickname = 22
    email = 33
    role = 44

    @staticmethod
    def make_unique_nickname(nickname):
        pass
        
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

        
    def __repr__(self):
        return '<User %r>' % (self.nickname)    
        

        

