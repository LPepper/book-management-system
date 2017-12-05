from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
borrow = Table('borrow', post_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('reader_no', String(length=40)),
    Column('book_id', String(length=40)),
    Column('borrow_date', DateTime),
    Column('return_date', DateTime),
)

book_style = Table('book_style', post_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('num', String(length=40)),
    Column('name', String(length=40)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['borrow'].columns['id'].create()
    post_meta.tables['book_style'].columns['id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['borrow'].columns['id'].drop()
    post_meta.tables['book_style'].columns['id'].drop()
