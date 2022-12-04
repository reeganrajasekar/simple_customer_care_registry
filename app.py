from flask import Flask, render_template , request , redirect , session
import ibm_db


conn_str=''
conn = ibm_db.connect(conn_str,'','')
 

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'nmc8so7c0no78ypw9o8b[np0'

@app.route("/db",methods=['GET'])
def db():
   sql = "create table kavi_query (id integer not null GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),email varchar(500),name varchar(500),query varchar(500),data varchar(50),PRIMARY KEY (id));"
   stmt = ibm_db.exec_immediate(conn, sql)
   sql = "create table kavi_users (id integer not null GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),name varchar(500),email varchar(500),password varchar(225),mob varchar(50),PRIMARY KEY (id));"
   stmt = ibm_db.exec_immediate(conn, sql)
   return "ok"


@app.route("/",methods = ['GET'])
def index():
    return render_template("login.html")

@app.route("/signin",methods = ['POST'])
def index_signin():
    sql = "select * from kavi_users where email='"+request.form["email"]+"'"
    stmt = ibm_db.exec_immediate(conn, sql)
    data = []
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        data.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)
    if(data):
        if(data[0]["PASSWORD"]==request.form["password"]):
            session["user"]=data[0]["ID"]
            session["name"]=data[0]["NAME"]
            session["email"]=data[0]["EMAIL"]
            return redirect("/user")
        else:
            return redirect("/")
    else:
        return redirect("/")

@app.route("/register",methods = ['GET'])
def index_register():
    return render_template("register.html")

@app.route("/signup",methods = ['POST'])
def index_signup():
    sql = "INSERT INTO kavi_users (name , email , password,mob)values('"+request.form["name"]+"','"+request.form["email"]+"','"+request.form["password"]+"','"+request.form["mob"]+"')"
    stmt = ibm_db.exec_immediate(conn, sql)
    return redirect("/")
    

# USER

@app.route("/user/",methods = ['GET'])
def user():
    sql = "SELECT * FROM kavi_query where email='"+session["email"]+"'"
    data=[]
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        data.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)
    return render_template("user/index.html",data=data)

@app.route("/user/create",methods = ['POST'])
def user_create():
    sql = "INSERT INTO kavi_query (email,name , query , data)values('"+session["email"]+"','"+request.form["title"]+"','"+request.form["query"]+"','Waiting List')"
    stmt = ibm_db.exec_immediate(conn, sql)
    return redirect("/user")


@app.route("/user/logout",methods = ['GET'])
def user_logout():
    return redirect("/")


# Admin


@app.route("/admin",methods = ['GET'])
def admin():
    return render_template("admin/login.html")

@app.route("/admin",methods = ['POST'])
def admin_signin():
    if(request.form["email"]=="admin@gmail.com"):
        if(request.form["password"]=="admin"):
            return redirect("/admin/home")
        else:
            return redirect("/admin")
    else:
        return redirect("/admin")

@app.route("/admin/home",methods = ['GET'])
def admin_home():
    sql = "SELECT * FROM kavi_query"
    data=[]
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        data.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)
    return render_template("admin/index.html",data=data)

@app.route("/admin/update/<id>",methods = ['POST'])
def query_update(id):
    sql = "UPDATE kavi_query set data='"+request.form["data"]+"' where id='"+id+"'"
    stmt = ibm_db.exec_immediate(conn, sql)
    return redirect("/admin/home")


@app.route("/admin/logout",methods = ['GET'])
def admin_logout():
    return redirect("/")



if __name__ == '__main__':
   app.run()