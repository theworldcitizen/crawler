
from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import Model


class News(Model):
    __tablename__ = 'Novosti'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    publication_date = Column(String)
    link = Column(String)


# class Password(db.Model):
#     __tablename__ = 'Password'
#     password = Column(String)





