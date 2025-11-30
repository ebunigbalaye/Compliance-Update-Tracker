from sqlalchemy import create_engine,MetaData,Table,Column,String,insert,select,update,delete,Computed,Boolean
import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'app_database.db')


engine = create_engine(f"sqlite:///{db_path}",echo=False)
metadata = MetaData()

subscribers_table = Table(
        "subscribers",
          metadata,
        Column("email", String(255), primary_key=True), 
        Column("name", String(255), nullable=False))
      
  

def add_subscriber(name:str,email:str):
    with engine.connect() as database_connection:
        insert_statement = insert(subscribers_table).prefix_with('OR IGNORE').values(name=name, email=email)   
        database_connection.execute(insert_statement)
        database_connection.commit()

def search_subscriber(email):
    """Search for a user in the database, the search parameter is the column name and the search_item is 
    the user to be found"""
    with engine.connect() as database_connection:
        search_statement = select(subscribers_table).where(subscribers_table.c.email == email)
        users = database_connection.execute(search_statement)
        user = users.first()
        if user is None:
        #Subscriber not found
            return False
        return True


def return_subscribers():
    subscribers = []
    with engine.connect() as database_connection:
        view_statement = select(subscribers_table.c)
        existing_subscribers = database_connection.execute(view_statement)
        for row in existing_subscribers.fetchall():
            subscribers.append(row)
        return subscribers

def search_subscriber(email):
    """Search for a subscriber in the database, the search parameter is the column name and the search_item is 
    who is the email be found"""
    with engine.connect() as database_connection:
        search_statement = select(subscribers_table).where(subscribers_table.c.email == email)
        subscribers = database_connection.execute(search_statement)
        subscriber = subscribers.first()
        if subscriber is None:
            return False
        else:
            return True

articles_table = Table(
        "articles",
          metadata,
        Column("link", String(255), primary_key=True), 
        Column("title", String(255), nullable=False),
        Column("description", String(255), nullable=False),
        Column("pub_date", String(255),nullable=False),
        Column("content", String(255),nullable=False),
        Column("compliance", Boolean,nullable=False))

def add_article(title:str,link:str,description:str,pub_date:str,content:str,compliance:bool):
    with engine.connect() as database_connection:
        insert_statement = insert(articles_table).prefix_with('OR IGNORE').values(title=title,link=link,description=description,pub_date=pub_date,content=content,compliance=compliance)   
        database_connection.execute(insert_statement)
        database_connection.commit()

def return_articles():
    """This function returns a list of articles """
    articles = []
    with engine.connect() as database_connection:
      view_statement = select(articles_table.c)
      article_table = database_connection.execute(view_statement)
      for article in article_table.fetchall():
          articles.append(article)
      return articles
    

metadata.create_all(engine)

