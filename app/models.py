from app import db

class Book_style(db.Model):
    __tablename__='book_style'
    id = db.Column(db.INTEGER, primary_key=True)
    num=db.Column(db.String(40),index = True,unique=True)
    name=db.Column(db.String(40))

    def __repr__(self):
        return '<Book_style %r>' % (self.num)

class Reader(db.Model):
    __tablename__ = 'reader'
    no=db.Column(db.String(40),primary_key=True,unique=True)
    name=db.Column(db.String(40))
    gender=db.Column(db.String(10))
    kind=db.Column(db.INTEGER)
    password=db.Column(db.String(40))
    phone=db.Column(db.String(40),default='0')
    grade=db.Column(db.String(40))
    department=db.Column(db.String(40))

    def __repr__(self):
        return '<Reader %r>' % (self.no)

class Book(db.Model):
    __tablename__ = 'book'
    id=db.Column(db.String(40),primary_key=True,unique=True)
    name = db.Column(db.String(40))
    style_num=db.Column(db.String(40))
    author=db.Column(db.String(20))
    count=db.Column(db.INTEGER,default=0)
    available_count = db.Column(db.INTEGER, default=0)
    price=db.Column(db.FLOAT,default=0)
    press=db.Column(db.String(40))
    publish_date=db.Column(db.String(40))
    summary=db.Column(db.String(80))

    def __repr__(self):
        return '<Book %r>' % (self.id)

class Borrow(db.Model):
    __tablename__ = 'borrow'
    id = db.Column(db.INTEGER, primary_key=True)
    reader_no=db.Column(db.String(40),db.ForeignKey('reader.no'),index = True)
    book_id=db.Column(db.String(40),db.ForeignKey('book.id'))
    borrow_date=db.Column(db.DateTime)
    return_date=db.Column(db.DateTime)

    def __repr__(self):
        return '<Borrow %r>' % (self.reader_no)

class Return_info(db.Model):
    __tablename__ = 'return_info'
    id = db.Column(db.INTEGER, primary_key=True)
    reader_no = db.Column(db.String(40),db.ForeignKey('reader.no'),index = True)
    book_id = db.Column(db.String(40),db.ForeignKey('book.id'))
    borrow_date = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime)
    overday=db.Column(db.INTEGER,default=0)

    def __repr__(self):
        return '<Return_info %r>' % (self.reader_no)