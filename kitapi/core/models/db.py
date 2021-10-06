import os

import sqlalchemy
from sqlalchemy.orm import sessionmaker


engine = sqlalchemy.create_engine(os.environ["PG_CONN_URL"])

SessionLocal = sessionmaker(autocommit=True, bind=engine)
