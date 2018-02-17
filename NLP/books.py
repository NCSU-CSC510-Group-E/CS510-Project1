from peewee import Model
from peewee import IntegerField
from peewee import TextField
from peewee import CharField
from peewee import ForeignKeyField
from peewee import SqliteDatabase

db = SqliteDatabase('books.db')

class BaseModel(Model):
    class Meta:
        database = db
        
class Author(BaseModel):
    ID = IntegerField(primary_key=True)
    FirstName = CharField()
    LastName = CharField()
    
class Book(BaseModel):
    ID = IntegerField(primary_key=True)
    Title = CharField()
    Author = ForeignKeyField(Author, backref='authors')

class Topic(BaseModel):
    ID = IntegerField(primary_key=True)
    Text = CharField()
    Book = ForeignKeyField(Book, backref='books')


db.connect()
db.create_tables([Author, Book, Topic], safe=True)
