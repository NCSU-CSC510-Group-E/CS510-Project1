from peewee import Model
from peewee import TextField
from peewee import CharField
from peewee import ForeignKeyField
from peewee import SqliteDatabase

db = SqliteDatabase('books.db')

class BaseModel(Model):
    class Meta:
        database = db
        
class Book(BaseModel):
    # ID = IntegerField()
    Title = CharField()

class Topic(BaseModel):
    # ID = IntegerField()
    Text = TextField()
    # Not sure what backref is for
    Book = ForeignKeyField(Book, backref='books')


db.connect()
db.create_tables([Book, Topic], safe=True)
