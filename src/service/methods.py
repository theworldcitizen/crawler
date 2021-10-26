from sqlalchemy import create_engine, select, delete, update, insert
from sqlalchemy import Table, Column, String, MetaData, Integer
from flask_sqlalchemy import Model

from conf import db
from src.crawler.crawler import Zakonkz
from src.models import News


class CRUD:

    def __init__(self):
        self.crawler = Zakonkz("https://www.zakon.kz/")
        self.conn = create_engine("postgresql+psycopg2://postgres:postgres@localhost/postgres", echo=False)
        self.meta = MetaData(self.conn)
        self.session = self.conn.connect()

        self.news = News
        # self.password = Password

    def insert_password(self):
        insert_statement = self.password.insert().values(password='123')
        self.session.execute(insert_statement)

    def create(self, one_news: dict):
        data = self.news.insert().values(title=one_news.get("title"), description=one_news.get("description"),
                                         publication_date=one_news.get("publish date"), link=one_news.get("link"))
        self.session.execute(data)

    def test_create(self):
        objects = self.crawler.loop()
        for object in objects:
            self.create(object)

    def get_password(self):
        res = self.password.select().where(self.password.c.password == '1')
        ans = self.session.execute(res).fetchone()._asdict()
        return ans

    def read_by_id(self, id: int):
        a = select(self.news).where(self.news.id == id)
        res = db.session.execute(a).first()[0].title
        print(type(res))
        return res

    def read_by_url(self, url: str):
        a = self.news.select().where(self.news.c.link == url)
        res = self.session.execute(a).fetchone()._asdict()
        return res

    def update(self, object_: dict):
        link = object_.get('link')
        update_query = self.news.update().where(self.news.c.link == link).values(title=object_.get("title"),
                                                                                 description=object_.get("description"),
                                                                                 publication_date=object_.get(
                                                                                     "publish date"),
                                                                                 link=object_.get("link"))
        result = self.session.execute(update_query)
        return result

    def delete(self, id: int):
        delete_query = self.news.delete().where(self.news.id == id)
        result = self.session.execute(delete_query)
        return result

    # def main(self):
    #     # a = self.test_create()
    #     b = self.test_read()
    #     # self.test_update()
    #     return b


if __name__ == "__main__":
    # # answer = CRUD().update(12, {'title': 'Updated', 'description': 'updated', 'publication_date': 'updated date',
    # #                             'link': "https://www.zakon.kz//5085804-v-kazahstane-zapretyat-est-koshek-i.html"})
    answer = CRUD().read_by_id(5)
    print(answer)
