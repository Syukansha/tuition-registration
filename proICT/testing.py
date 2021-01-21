import os
import cx_Oracle
from flask import Flask,render_template,redirect,url_for,request,session,flash
from datetime import timedelta


db_user = os.environ.get('DBAAS_USER_NAME', 'KANSHA')
db_password = os.environ.get('DBAAS_USER_PASSWORD', '123')
db_connect = os.environ.get('DBAAS_DEFAULT_CONNECT_DESCRIPTOR', "localhost:1521/xe")
service_port = port=os.environ.get('PORT', '8080')
app = Flask(__name__)

app.secret_key = 'hello'
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/',methods=["POST","GET"])
def login():

      conn = cx_Oracle.connect(db_user, db_password, db_connect)
      cur= conn.cursor()

      if request.method == "POST":
          session.permanent = True
          user = request.form['uname']
          password = request.form['psw']
          sql = """select admin_name,admin_password from admins where admin_name=(:Aname) and admin_password=(:Apassword) """
          cur.execute(sql,{"Aname":user, 'Apassword':password})
          result = cur.fetchone()
          conn.commit()
          if len(result)>0:
              session["user"] = user
              flash('Login successful')
              return redirect(url_for('user'))
          else:
              flash('user cannot found')
              return render_template('login_try.html')

      else:

           if "user" in session:
                  flash("Already logged in!")
                  return redirect(url_for("user"))
           return render_template("login_try.html")

       


@app.route("/user")
def user():
    if "user" in session:
        session.permanent = True
        user= session["user"]
        conn = cx_Oracle.connect(db_user, db_password, db_connect)
        cur = conn.cursor()
        cur.execute("select * from admins")
        data = cur.fetchall()
        return render_template('user.html',user=user,data=data)
    else:
        flash('You not logged in')
        return redirect(url_for("login"))
      
    


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logout", 'info')
    return redirect(url_for("login"))

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
      app.run(debug=True,port=5001)