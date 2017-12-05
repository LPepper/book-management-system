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
)

reader = Table('reader', post_meta,
    Column('no', String(length=40), primary_key=True, nullable=False),
    Column('name', String(length=40)),
    Column('gender', String(length=10)),
    Column('kind', INTEGER),
    Column('password', String(length=40)),
    Column('phone', String(length=40), default=ColumnDefault('0')),
    Column('grade', String(length=40)),
    Column('department', String(length=40)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['book'].columns['press'].create()
    post_meta.tables['book'].columns['publish_date'].create()
    post_meta.tables['reader'].columns['department'].create()
    post_meta.tables['reader'].columns['grade'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['book'].columns['press'].drop()
    post_meta.tables['book'].columns['publish_date'].drop()
    post_meta.tables['reader'].columns['department'].drop()
    post_meta.tables['reader'].columns['grade'].drop()
