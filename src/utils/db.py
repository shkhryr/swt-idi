from sqlalchemy import (    create_engine,    Table,    MetaData,    Column,    Integer,    String,    insert,)from sqlalchemy.orm import declarative_base, Sessionfrom sqlalchemy.sql import existsfrom dotenv import load_dotenv, find_dotenvfrom os import getenvload_dotenv(find_dotenv())engine = create_engine(getenv("DB_URL"))Base = declarative_base()metadata_obj = MetaData()session = Session(engine)class User(Base):    __tablename__ = 'user_account'    id = Column(Integer, primary_key=True)    tg_id = Column(Integer, unique=True)    gender = Column(String(20))    age = Column(Integer)Base.metadata.create_all(engine)user_table = Table('user_account', metadata_obj, autoload_with=engine)async def write_user(tg_id, gender, age):    with engine.connect() as conn:        create_user = insert(user_table).values(            tg_id=tg_id,            gender=gender,            age=age        )        conn.execute(create_user)def user_exists(tg_id):    with engine.connect() as conn:        q = session.query(exists().where(User.tg_id == tg_id)).scalar()        return qasync def register_user(tg_id, age, gender):    with engine.connect() as conn:        create_user = insert(user_table).values(            tg_id=tg_id,            age=age,            gender=gender,        )        conn.execute(create_user)        session.commit()        return 'USER HAS BEEN REGISTERED SUCCESSFULLY!'