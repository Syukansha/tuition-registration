import os
import cx_Oracle
from flask import Flask,render_template,redirect,url_for,request,session,flash
from datetime import timedelta


db_user = os.environ.get('DBAAS_USER_NAME', 'TUITION')
db_password = os.environ.get('DBAAS_USER_PASSWORD', '123')
db_connect = os.environ.get('DBAAS_DEFAULT_CONNECT_DESCRIPTOR', "localhost:1521/xe")
service_port = port=os.environ.get('PORT', '8080')
app = Flask(__name__)

app.secret_key = 'hello'
app.permanent_session_lifetime = timedelta(minutes=30)


#####################################################STAFF################################################################
@app.route('/',methods=["POST","GET"])
def login():

      conn = cx_Oracle.connect(db_user, db_password, db_connect)
      cur= conn.cursor()

      if request.method == "POST":
          session.permanent = True
          user = request.form['uname']
          password = request.form['psw']
          sql = """select staff_name,password from STAFF where staff_name=(:Aname) and password=(:Apassword) """
          cur.execute(sql,{"Aname":user, 'Apassword':password})
          result = cur.fetchone()
          conn.commit()
          
            
          if  result == None:
              flash('user cannot found')
              return render_template('login2.html')
            
          elif len(result) > 0:
            session["user"] = user
            flash('Login successful!')
            return redirect(url_for('user'))

      else:

           if "user" in session:
                  flash("Already logged in!")
                  return redirect(url_for("user"))
           return render_template("login2.html")

@app.route("/user")
def user():
    if "user" in session:
        session.permanent = True
        user= session["user"]
        conn = cx_Oracle.connect(db_user, db_password, db_connect)
        cur = conn.cursor()
        cur.execute("select * from staff")
        data = cur.fetchall()
        return render_template('user.html',user=user,data=data)
    else:
        flash('You not logged in')
        return redirect(url_for("login"))
      
@app.route('/user/registerStaff')
def addUser():
    return render_template('registerStaff.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logout", 'info')
    return redirect(url_for("login"))

@app.route('/user/registerStaff/submit', methods=['POST','GET'])
def add():
   
    conn = cx_Oracle.connect(db_user, db_password, db_connect)
    cur = conn.cursor()
    fullname = request.form['name']
    idNumber = request.form['staffid']
    Apassword = request.form['password']
    sql = """insert into staff(staff_id,staff_name,password) values (:id,:name,:password)"""
    cur.execute(sql,{'id':idNumber,'name':fullname ,'password':Apassword})
    conn.commit()
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/delete')
def delete():
    return render_template('delete.html')

@app.route('/deleteUser/<string:id_data>', methods=['GET'])
def deleteUSer(id_data):
    conn = cx_Oracle.connect(db_user, db_password, db_connect)
    cur = conn.cursor()
    sql = "DELETE FROM staff WHERE staff_id=(:id)"
    cur.execute(sql,{"id":id_data})
    conn.commit()
    return redirect(url_for('success'))

@app.route('/user/updateStaff/<string:iddata>/<string:namedata>/<string:passworddata>',methods=["GET"])
def update(iddata,namedata,passworddata):
    return render_template('updateStaff.html',data=iddata,data2=namedata,data3=passworddata)

@app.route('/user/updateStaff', methods=['POST','GET'])
def updateCust():
    conn = cx_Oracle.connect(db_user, db_password, db_connect)
    cur = conn.cursor()
    if request.method == "POST":
        adminId = request.form['id']
        fullname = request.form['name']
        Apassword = request.form['Apassword']
        sql = """update staff set staff_name=(:name),password=(:password) where staff_id=(:id)"""
        cur.execute(sql,{'name':fullname,'password':Apassword,'id':adminId})
        conn.commit()
        return redirect(url_for('success'))
    


@app.route('/homeAI')
def homeAI():
    return render_template('student_record.html')

#######################################student#############################################################################

@app.route('/user/student')
def student():
    conn = cx_Oracle.connect(db_user, db_password, db_connect)
    cur = conn.cursor()
    cur.execute("select * from student")
    data = cur.fetchall()
    return render_template('student record.html',user=user,data=data)

@app.route('/user/type')
def register():
    return render_template('type.html')

@app.route('/user/type/stuRegister')
def registerStud():
    return render_template('register.html')

@app.route('/deleteStudent/<string:id_student>', methods=['GET'])
def deleteStud(id_student):
    conn = cx_Oracle.connect(db_user, db_password, db_connect)
    cur = conn.cursor()
    sql = "DELETE FROM student WHERE stu_id=(:id)"
    cur.execute(sql,{"id":id_student})
    conn.commit()
    return redirect(url_for('success'))


@app.route('/user/addStudent', methods=['POST','GET'])
def addStud():
    conn = cx_Oracle.connect(db_user, db_password, db_connect)
    cur = conn.cursor()

    firstname = request.form['first_name'] 
    lastName = request.form['last_name'] 
    studentEmail = request.form['email']
    studentNum = request.form['phone_num'] 
    studentAddress = request.form['address'] 
    
    sql =  """insert into student(stu_id,stu_fname,stu_lname,stu_no,stu_email,stu_address) values (stu_id.nextval,:firstname,:lastname,:stunum,:stuemail,:stuaddress)"""
    cur.execute(sql,{'firstname':firstname,'lastname':lastName,'stunum':studentNum,'stuemail':studentEmail,'stuaddress':studentAddress})
    conn.commit()
    return redirect(url_for('success'))

@app.route('/user/deleteStudent/<string:id_data>', methods=['POST','GET'])
def deleteStudent(id_data):
    conn = cx_Oracle.connect(db_user, db_password, db_connect)
    cur = conn.cursor()

    sql2 = """ delete from enroll where stu_id=(:sid) """
    cur.execute(sql2,{"sid":id_data})
    conn.commit()
    sql3 = """ delete from payment where stu_id=(:stid) """
    cur.execute(sql3,{"stid":id_data})
    conn.commit()
    sql = "DELETE FROM student WHERE stu_id=(:id)"
    cur.execute(sql,{"id":id_data})
    conn.commit()
    return redirect(url_for('success'))

@app.route('/user/studentUpdate/<string:iddata>/<string:fnamedata>/<string:lnamedata>/<string:phonedata>/<string:emaildata>/<string:addrdata>',methods=["GET"])
def studentUpdate(iddata,fnamedata,lnamedata,phonedata,emaildata,addrdata):
    conn = cx_Oracle.connect(db_user, db_password, db_connect)
    cur = conn.cursor()
    sql = """ select  tot_amout,payment_status,invoice_no from payment where stu_id = (:stuid) """
    cur.execute(sql,{'stuid':iddata})
    data = cur.fetchall()
    return render_template('updateStudent.html',data=data,data1=iddata,data2=fnamedata,data3=lnamedata,data4=phonedata,data5=emaildata,data6=addrdata)

@app.route('/user/student/updateStudent/submit', methods=['POST','GET'])
def submitUpdate():
    conn = cx_Oracle.connect(db_user, db_password, db_connect)
    cur = conn.cursor()
    
    if request.method == 'POST':
        studentID = request.form['stuid']
        stuID = request.form['stuid']
        firstname = request.form['first_name'] 
        lastName = request.form['last_name'] 
        studentEmail = request.form['email']
        studentNum = request.form['phone_num'] 
        studentAddress = request.form['address'] 
        status = request.form['status']
        amount = request.form['fee']
        invoice = request.form['invoice']

        sql =   """update student set stu_fname=(:fname),stu_lname=(:lname),stu_no=(:num),stu_email=(:email),stu_address=(:address) where stu_id=(:stuid)"""
        cur.execute(sql,{'stuid':studentID,'fname':firstname,'lname':lastName,'num':studentNum,'email':studentEmail,'address':studentAddress})
        conn.commit()
        
        sql2 = """update payment set tot_amout=(:amount),payment_status=(:status) where stu_id=(:sid) and invoice_no=(:inv)"""
        cur.execute(sql2,{'sid':stuID,'status':status,'amount':amount,'inv':invoice})
        conn.commit()
        return redirect(url_for('success'))




@app.route('/user/student/view/<string:iddata>/<string:fnamedata>/<string:lnamedata>')
def viewStudent(iddata,fnamedata,lnamedata):
    conn = cx_Oracle.connect(db_user, db_password, db_connect)
    cur = conn.cursor()
    sql = """ select invoice_no, tot_amout, payment_status from payment e join enroll d 
                on e.stu_id = d.stu_id  where e.stu_id=(:stuid)"""
    cur.execute(sql,{'stuid':iddata})
    data = cur.fetchall()
    sql2 = """ select subject_id from enroll  where stu_id = (:stuid) """
    cur.execute(sql2,{'stuid':iddata})
    data1 = cur.fetchall()

    sql3 = """ select class_id from class d join enroll e using(subject_id) where stu_id = (:stuid) """
    cur.execute(sql3,{'stuid':iddata})
    dataS = cur.fetchall()
    return render_template('view_student_record.html',data=data,dataS=dataS,data1=data1,data2=fnamedata,data3=lnamedata)


##################################################Subject####################################################################

@app.route('/user/registerSubject/<string:stuid>')
def registerSubject(stuid):
    conn = cx_Oracle.connect(db_user, db_password, db_connect)
    cur = conn.cursor()
    sql = """ select subject_id from enroll where stu_id=(:stid) """
    cur.execute(sql,{'stid':stuid})
    data1 = cur.fetchall()

    return render_template('registerSubject.html',data=stuid,data1=data1,)

@app.route('/user/registerSubject/submit', methods=['POST','GET'])
def regSub():
    conn = cx_Oracle.connect(db_user, db_password, db_connect)
    cur = conn.cursor()
    if request.method == "POST":
        studentID = request.form['stu_id']
        staffID = request.form['staffid']
        subject = request.form.getlist('subject')
        alsub = request.form.getlist('alsub')
        totalAmount = len(subject) * 70
        for i in range(len(subject)):
            subject_id = subject[i]
            sql = """insert into enroll(enroll_id,stu_id,subject_id) values (enroll_id.nextval,:stuID,:subid)  """
            cur.execute(sql,{'stuid':studentID,'subid':subject_id})
            conn.commit()   
        sql2 = """ insert into payment(invoice_no,tot_amout,staff_id,payment_status,stu_id) values(invoice_no.nextval,:total,:staff,'not paid',:stuid) """
        cur.execute(sql2,{'total':totalAmount,'staff':staffID,'stuid':studentID})
        conn.commit()   
        return redirect(url_for('success'))


@app.route('/user/dropSubjects/<string:stuid>')
def dropSubject(stuid):
    conn = cx_Oracle.connect(db_user, db_password, db_connect)
    cur = conn.cursor()
    sql = """ select subject_id from enroll where stu_id=(:stid) """
    cur.execute(sql,{'stid':stuid})
    data1 = cur.fetchall()
    sql2 = """ select staff_id from payment  where stu_id=(:stid) """
    cur.execute(sql2,{'stid':stuid})
    data2 = cur.fetchall()
    return render_template('dropSubjects.html',data=stuid,data1=data1,data2=data2)


@app.route('/user/dropSubjects/submit', methods=['POST','GET'])
def dropSub():
    conn = cx_Oracle.connect(db_user, db_password, db_connect)
    cur = conn.cursor()
    if request.method == "POST":
        studentID = request.form['stu_id']
        staffID = request.form['staffid']
        subject = request.form.getlist('subject')
        alsub = request.form.getlist('alsub')
        
        for i in range(len(subject)):
            subject_id = subject[i]
            sql = """ delete from enroll where subject_id = (:subid) and stu_id=(:stuid)"""
            cur.execute(sql,{'subid':subject_id,'stuid':studentID})
            conn.commit()
    
        return redirect(url_for('success'))



#####################################teachers############################################################################
@app.route('/user/teachers')
def teachers():
    conn = cx_Oracle.connect(db_user, db_password, db_connect)
    cur = conn.cursor()
    cur.execute("select * from teacher")
    data = cur.fetchall()
    return render_template('teachers_record.html',data=data)

@app.route('/deleteTeachers/<string:id_teachers>', methods=['GET'])
def deleteTeach(id_teachers):
    conn = cx_Oracle.connect(db_user, db_password, db_connect)
    cur = conn.cursor()
    sql = "DELETE FROM teacher WHERE teacher_id=(:id)"
    cur.execute(sql,{"id":id_teachers})
    conn.commit()
    return redirect(url_for('success'))

@app.route('/user/type/registerTeacher')
def registerTeacher():
    return render_template('registerTeacher.html')

@app.route('/user/type/registerTeacher/submit', methods=['POST','GET'])
def regTeach():
    conn = cx_Oracle.connect(db_user, db_password, db_connect)
    cur = conn.cursor()
    if request.method == 'POST':
        teacherName = request.form['name']
        pnum = request.form['phone_num']
        email = request.form['email']
        hiredate = request.form['date']
 
        sql = "insert into teacher(teacher_id,teacher_name,teacher_no,teacher_email,hire_date) values(teacher_id.nextval,:name,:num,:email,to_date(:hiredate,'dd/mm/yyyy'))"
        cur.execute(sql,{'name':teacherName,'num':pnum,'email':email,'hiredate':hiredate})
        conn.commit()
        return redirect(url_for('success'))


@app.route('/user/teachers/updateTeachers/<string:iddata>/<string:namedata>/<string:phonedata>/<string:emaildata>/<string:datedata>')
def teachersUpdate(iddata,namedata,phonedata,emaildata,datedata):
    return render_template('updateTeachers.html',data1=iddata,data2=namedata,data3=phonedata,data4=emaildata,data5=datedata)


@app.route('/user/teachers/updateTeachers/submit', methods=['POST','GET'])
def submitUpdateTeach():
    conn = cx_Oracle.connect(db_user, db_password, db_connect)
    cur = conn.cursor()
    
    if request.method == 'POST':
        tID = request.form['tid']
        name = request.form['name']
        email= request.form['email']
        phonenum = request.form['phone_num']
        hire = request.form['date']

        sql =   """update teacher set teacher_name=(:name),teacher_no=(:num),teacher_email=(:email), hire_date= to_date(:hire,'dd/mm/yyyy') where teacher_id=(:tid)"""
        cur.execute(sql,{'tid':tID,'name':name,'num':phonenum,'email':email,'hire':hire})
        conn.commit()
        return redirect(url_for('success'))


@app.route('/user/teachers/view/<string:iddata>/<string:fnamedata>/<string:numdata>/<string:emaildata>/')
def viewTeacher(iddata,fnamedata,numdata,emaildata):
    conn = cx_Oracle.connect(db_user, db_password, db_connect)
    cur = conn.cursor()
    sql = """ select hire_date, class_id from teacher e join class d on e.teacher_id = d.teacher_id where e.teacher_id = (:tid) """
    cur.execute(sql,{'tid':iddata})
    data = cur.fetchall()
    return render_template('view_teacher record.html',data=data,data1=iddata,data2=fnamedata,data3=numdata,data4=emaildata)

if __name__ == '__main__':
      app.run(debug=True,port=5001)
 

