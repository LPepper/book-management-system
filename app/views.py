from app import app,models,db,forms

from sqlalchemy import or_,and_
from flask import  render_template,url_for,flash,redirect,session,request
import datetime

#用户登录
@app.route('/',methods=['GET','POST'])
def login():
    form=forms.LoginForm()
    if form.validate_on_submit():
        reader=models.Reader.query.filter_by(no=form.name.data).first()
        if reader is None:
            flash('用户名不存在')
        elif reader.password == form.password.data:
            if reader.kind==2:
                flash('你好,'+reader.name)
                return redirect('/manager')
            else:
                session['user']=reader.no
                flash('你好,'+reader.name)
                return redirect('/search')
        else:
            flash('密码错误')

    return render_template('login.html',form=form)

#书籍查询
@app.route('/search',methods=['GET','POST'])
def search():
    reader_no=session['user']
    form =forms.SearchForm()
    if form.validate_on_submit():
        data=form.bookinfo.data.strip()#去掉首位空格

        book=[]
        if data.find(' ')<0:
            # 单条件查询
            book=models.Book.query.filter(or_(models.Book.name.like('%'+data+'%'),
                                            models.Book.id==data,
                                             models.Book.author.like('%'+data+'%'),
                                            models.Book.press.like('%'+data+'%'),
                                            models.Book.summary.like('%' + data + '%'),
                                            models.Book.publish_date.like('%' + data + '%'))).all()
        else:
            # 组合查询
            c=data.split()
            length=len(c)
            count=0
            result = models.Book.query.filter(or_(models.Book.name.like('%' + c[count] + '%'),
                                                 models.Book.id == data,
                                                 models.Book.author.like('%' + c[count] + '%'),
                                                 models.Book.press.like('%' + c[count] + '%'),
                                                 models.Book.summary.like('%' + c[count] + '%'),
                                                 models.Book.publish_date.like('%' + c[count] + '%'))).all()
            bookset=set(result)
            count+=1
            #用set找出and匹配元素
            while count<length:
                result = models.Book.query.filter(or_(models.Book.name.like('%' + c[count] + '%'),
                                                    models.Book.id == data,
                                                    models.Book.author.like('%' + c[count] + '%'),
                                                    models.Book.press.like('%' + c[count] + '%'),
                                                    models.Book.summary.like('%' + c[count] + '%'),
                                                    models.Book.publish_date.like('%' + c[count] + '%'))).all()
                bookset=bookset&set(result)
                count+=1

            book=list(bookset)

        if book ==[]:
            flash('无搜索结果')
        else:
            return render_template('aftersearch.html',books=book)
    return render_template('search.html',form=form,reader_no=reader_no)

@app.route('/manager',methods=['GET','POST'])
def manager():
    return render_template('manager.html')
#增加图书
@app.route('/manager/addbook',methods=['GET','POST'])
def addbook():
    form=forms.Book_add()
    if form.validate_on_submit():
        newbook= models.Book(id=form.id.data,
                             name=form.name.data,
                             style_num=form.style_num.data,
                             author=form.author.data,
                             count=form.count.data,
                             available_count=form.available_count.data,
                             price=form.price.data,
                             press=form.press.data,
                             publish_date=form.publish_date.data,
                             summary=form.summary.data)
        db.session.add(newbook)
        db.session.commit()
        flash('操作成功')
    return render_template('addbook.html',form=form)
#删除书籍
@app.route('/manager/deletebook',methods=['GET','POST'])
def deletebook():
    form=forms.Book_delete()
    if form.validate_on_submit():
        book= models.Book.query.filter_by(id=form.id.data).first()
        if book is None:
            flash('操作失败，不存在此书')
        else:
            borrowinfo=models.Borrow.query.filter_by(book_id=form.id.data).first()
            if borrowinfo is  None:
                db.session.delete(book)
                db.session.commit()
                flash('操作成功')
            else:
                flash('有读者尚未归还此书')
    return render_template('deletebook.html',form=form)
#增加读者
@app.route('/manager/addreader',methods=['GET','POST'])
def addreader():
    form=forms.Reader_add()
    if form.validate_on_submit():
        newreader= models.Reader(no=form.no.data,
                               name=form.name.data,
                               gender=form.gender.data,
                               kind=form.kind.data,
                               password=form.password.data,
                               phone=form.phone.data,
                               grade=form.grade.data,
                                department=form.department.data
                             )
        db.session.add(newreader)
        db.session.commit()
        flash('操作成功')
    return render_template('addreader.html',form=form)
#删除读者
@app.route('/manager/deletereader',methods=['GET','POST'])
def deletereader():
    form=forms.Reader_delete()
    if form.validate_on_submit():
        reader= models.Reader.query.filter_by(no=form.no.data).first()
        if reader is None:
            flash('操作失败，读者不存在')
        else:
            borrowlist=models.Borrow.query.filter_by(reader_no=form.no.data).all()
            if borrowlist!=[]:
                flash('该读者有图书尚未归还')
                return render_template('deletereaderfail.html')
            db.session.delete(reader)
            db.session.commit()
            flash('操作成功')

    return render_template('deletereader.html',form=form)

#书籍借阅
@app.route('/borrow/<bookid>',methods=['GET','POST'])
def borrow(bookid):
    a=models.Borrow.query.filter_by(reader_no=session['user']).all()
    for p in a:
        if datetime.datetime.now()>p.return_date :
            flash('您有超期图书未归还')
            return render_template('afterborrow.html')

    for p in a:
        if p.book_id==bookid :
            flash('您已借过此书')
            return render_template('afterborrow.html')
    b=models.Borrow(reader_no=session['user'],
                    book_id=bookid,
                    borrow_date=datetime.datetime.now(),
                    return_date=datetime.datetime.now()+datetime.timedelta(days=30))
    book=models.Book.query.filter_by(id=bookid).first()
    book.available_count-=1
    db.session.add(b)
    db.session.commit()
    flash('操作成功')
    return render_template('afterborrow.html')

#我的归还
@app.route('/returninfo',methods=['GET','POST'])
def returnifo():
    returnlist = models.Return_info.query.filter_by(reader_no=session['user']).all()
    booklist=models.Book.query.all()
    return render_template('returninfo.html',returnlist=returnlist,booklist=booklist)
#我的信息
@app.route('/myinfo',methods=['GET','POST'])
def myinfo():
    reader = models.Reader.query.filter_by(no=session['user']).first()
    return render_template('myinfo.html',reader=reader)
#读者借阅查询
@app.route('/borrowinfo',methods=['GET','POST'])
def borrowinfo():
    booklist=models.Book.query.all()
    returnlist=[]
    borrowlist=models.Borrow.query.filter_by(reader_no=session['user']).all()

    return  render_template('borrowinfo.html',borrowlist=borrowlist,booklist=booklist)

#修改图书查询
@app.route('/bookalter',methods=['GET','POST'])
def bookalterselect():
    form=forms.Book_alter_select()
    if form.validate_on_submit():
        book=models.Book.query.filter_by(id=form.id.data).first()
        if book is None:
            flash('此书不存在')
        else:
            return redirect('/bookalter/%s'%book.id)


    return render_template('bookalterselect.html',form=form)


#修改图书
@app.route('/bookalter/<bookid>',methods=['GET','POST'])
def bookalter(bookid):
    book = models.Book.query.filter_by(id=bookid).first()

    form=forms.Book_alter()
    if form.validate_on_submit():
        book.id=form.id.data
        book.name=form.name.data
        book.style_num=form.style_num.data
        book.author=form.author.data
        book.count=form.count.data
        book.available_count=form.available_count.data
        book.price=form.price.data
        book.press=form.press.data
        book.publish_date=form.publish_date.data
        book.summary=form.summary.data
        db.session.commit()
        flash('操作成功')

    return render_template('bookalter.html',form=form)

#修改读者查询
@app.route('/readeralter',methods=['GET','POST'])
def readeralterselect():
    form=forms.Reader_alter_select()
    if form.validate_on_submit():
        reader=models.Reader.query.filter_by(no=form.no.data).first()
        if reader is None:
            flash('该读者不存在')
        else:
            return redirect('/readeralter/%s'%reader.no)


    return render_template('readeraltersearch.html',form=form)

#修改读者
@app.route('/readeralter/<readerno>',methods=['GET','POST'])
def readeralter(readerno):
    reader = models.Reader.query.filter_by(no=readerno).first()

    form=forms.Reader_add()
    if form.validate_on_submit():
        reader.no=form.no.data
        reader.name=form.name.data
        reader.gender=form.gender.data
        reader.kind=form.kind.data
        reader.password=form.password.data
        reader.phone=form.phone.data
        reader.grade=form.grade.data
        reader.department=form.department.data

        db.session.commit()
        flash('操作成功')

    return render_template('readeralter.html',form=form)

#书籍归还
@app.route('/return/<bookid>&<reader_no>',methods=['GET','POST'])
def book_return(bookid,reader_no):
    a=models.Borrow.query.filter_by(reader_no=reader_no,
                                    book_id=bookid).first()
    book=models.Book.query.filter_by(id=bookid).first()
    if book is not None:
        book.available_count+=1
    overday=(datetime.datetime.now()-a.return_date).days
    #超期天数
    if overday < 0:
        overday=0

    b=models.Return_info(reader_no=session['user'],
                         book_id=bookid,
                         borrow_date=a.borrow_date,
                         return_date=datetime.datetime.now(),
                         overday=overday)
    db.session.add(b)
    db.session.delete(a)
    db.session.commit()
    flash('操作成功')
    return render_template('afterreturn.html',overday=overday)

#读者查询
@app.route('/manager/readersearch',methods=['GET','POST'])
def readersearch():
    form=forms.Reader_select()
    if form.validate_on_submit():
        data = form.no.data.strip()  # 去掉首位空格
        readers=[]
        #单条件查询
        if data.find(' ')<0:
            readers = models.Reader.query.filter(or_(models.Reader.no.like('%' + data + '%'),
                                                    models.Reader.gender == data,
                                                     models.Reader.grade == data,
                                                    models.Reader.department == data,
                                                    models.Reader.name.like('%' + data + '%'))).all()
        else:
            # 组合查询
            c = data.split()
            length = len(c)
            count = 0
            result = models.Reader.query.filter(or_(models.Reader.no.like('%' + c[count] + '%'),
                                                     models.Reader.gender == c[count],
                                                     models.Reader.grade == c[count],
                                                     models.Reader.department == c[count],
                                                     models.Reader.name.like('%' + c[count] + '%'))).all()
            readerset = set(result)
            count+=1
            # 用set找出and匹配元素
            while count < length:
                result = models.Reader.query.filter(or_(models.Reader.no.like('%' + c[count] + '%'),
                                                        models.Reader.gender == c[count],
                                                        models.Reader.grade == c[count],
                                                        models.Reader.department == c[count],
                                                        models.Reader.name.like('%' + c[count] + '%'))).all()
                readerset=readerset&set(result)
                count += 1
            readers=list(readerset)
        if readers==[]:
            flash('null')
        return render_template('afterreadersearch.html',readers=readers)
    return render_template('readersearch.html',form=form)

#超期信息
@app.route('/manager/overday_info',methods=['GET','POST'])
def overday_info():
    borrowlist=models.Borrow.query.all()
    overday_info=[]
    for p in borrowlist:
        if datetime.datetime.now()>p.return_date :
            overday_info.append(p)

    return render_template('overday_info.html',overday_info=overday_info)

