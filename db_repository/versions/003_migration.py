from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
return_info = Table('return_info', post_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('reader_no', String(length=40)),
    Column('book_id', String(length=40)),
    Column('borrow_date', DateTime),
    Column('return_date', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['return_info'].columns['borrow_date'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['return_info'].columns['borrow_date'].drop()
