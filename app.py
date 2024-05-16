from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from flask import Flask


app = Flask(__name__)

engine = create_engine('sqlite:///chocolate_shop.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
session.commit()


