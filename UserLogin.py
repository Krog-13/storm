from flask_login import UserMixin


class UserLogin(UserMixin):

    def fromDB(self, user_id, db):
        #self.__user = db.getUser(user_id)
        self.__user = db.query.filter_by(id=user_id).first()
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user.id)

    def getName(self):
        return self.__user.id if self.__user else "Без имени"

    def getEmail(self):
        return self.__user.email if self.__user else "Без email"