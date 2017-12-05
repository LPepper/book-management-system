from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
book = Table('book', post_meta,
    Column('id', String(length=40), primary_key=True, nullable=False),
    Column('name', String(length=40)),
    Column('style_num', String(length=40)),
    Column('author', String(length=20)),
    Column('count', INTEGER, default=ColumnDefault(0)),
    Column('available_count', INTEGER, default=ColumnDefault(0)),
    Column('price', FLOAT, default=ColumnDefault(0)),
    Column('press', String(length=40)),
    Column('publish_date', String(length=40)),
    Column('summary', String(length=80)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['book'].columns['summary'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['book'].columns['summary'].drop()
