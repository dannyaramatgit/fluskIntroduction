from flask import Flask, render_template, request, flash
from forms import ContactForm
from flask_wtf.csrf import CSRFProtect
import sqlite3 as sql

app = Flask(__name__)

# Add this somewhere in your app's initialization
csrf = CSRFProtect(app)
app.secret_key = 'development key'
csrf.init_app(app)

@app.route('/contact', methods = ['GET', 'POST'])
def contact():
   form = ContactForm()
   
   if request.method == 'POST':
      if form.validate() == False:
         print(form.errors) 
         flash('All fields are required.')
         return render_template('contact.html', form = form)
      else:
         return 'success'
   elif request.method == 'GET':
      return render_template('contact.html', form = form)


@app.route('/enternew')
def new_student():
   return render_template('student.html')

@app.route('/list')
def list():
   con = sql.connect("mydb.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall(); 
   return render_template("list.html",rows = rows)

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         pin = request.form['pin']
         
         with sql.connect("mydb.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("student_result.html",msg = msg)
         con.close()


if __name__ == '__main__':
   app.run(debug = True)

