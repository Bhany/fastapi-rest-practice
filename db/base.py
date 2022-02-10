from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

ship_org = Table('ship_org', Base.metadata,
    Column('ship_id', ForeignKey('shipment.reference_id'), primary_key=True),
    Column('org_id', ForeignKey('organization.code'), primary_key=True)
)
