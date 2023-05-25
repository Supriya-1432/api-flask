from flask import Flask,render_template,request,redirect,session
from mysql.connector import connect

con=connect(host='localhost',port=3306,database='word',user='root')

app=Flask(__name__)
app.secret_key='hghfgfchhfhfh'

@app.route('/admin')
def admin():
    return render_template('admin_login.html')

@app.route('/adminlogin_validation',methods=["GET","POST"])
def adminlogin_validation():
    if request.method=="POST":
        email=request.form['email']
        password=request.form['password']
        session['admin']=password
        if (email=="admin123@gmail.com") and (password=='admin'):
            return render_template('Admin.html')
        else:
            return render_template('admin_login.html', response='Check ur credentials')
    else:
        return render_template('admin_login.html')

@app.route('/adminpanel')
def adminPanel():
    if session.get('admin'):
        return render_template('Admin.html')
    else:
        return redirect('/admin')

@app.route('/EditingWord',methods=["GET","POST"])
def EditingCaseInDb():
    if request.method=="POST":
        cur=con.cursor()
        cur.execute("select * from word")
        x=cur.fetchone()
        x=x[0]
        word=request.form['word']      
        cur.execute("update word SET word=%s where word=%s",(word,x))
        con.commit()
        return render_template('Admin.html')
    else:
        return redirect('/')

@app.route('/')
def getword():
    cur=con.cursor()
    cur.execute('select * from word')
    y=cur.fetchone()
    if y==None:
        cur=con.cursor()
        cur.execute("insert into word values(%s)",("Text",))
        con.commit()
        return render_template('viewword.html',word="Text")
    else:
        return render_template('viewword.html',word=y[0])

@app.route('/logoutadmin')
def logoutadmin():
    session['admin']=None
    return redirect('/')

if __name__=="__main__":
     app.run(debug=True)