from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "mysql://root:Ecommercemysql12$@localhost/todolistfastapi"
engine = create_engine(db_url)
sessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)