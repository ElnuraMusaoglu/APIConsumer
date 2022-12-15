import os
from databases import Database
from sqlalchemy import (
    create_engine, MetaData,
    Column, Table,
    Integer, String, DateTime
)
from sqlalchemy.sql import func


DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
metadata = MetaData()
groups = Table(
    'groups',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('description', String(100)),
    Column('transaction_id', String(100)),
    Column('transaction_timestamp', String(50)),
    Column('created_date', DateTime, default=func.now(), nullable=False)
)

groupdelete = Table(
    'groupdelete',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('transaction_id', String(100)),
    Column('transaction_timestamp', String(50)),
    Column('created_date', DateTime, default=func.now(), nullable=False)
)

database = Database(DATABASE_URL)
