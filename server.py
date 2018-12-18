from flask import Flask, render_template, redirect, session, request, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import re

app = Flask(__name__)
app.secret_key = "lol secrect key am i rite"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)

@app.route('/')
def login_page():
    return render_template('/login.html')

@app.route("/emailconfirm", methods=["post"])
def username():
    found = False
    mysql = connectToMySQL('handy_helper')
    query = "SELECT email_address from users WHERE users.email_address = %(em)s;"
    data = { 'em' : request.form['email'] }
    result = mysql.query_db(query, data)
    if result:
        found = True
    return render_template('emailconfirm.html', found=found)

@app.route('/register', methods=["post"])
def register():
    mysql=connectToMySQL('handy_helper')
    data = {
    "fn" : request.form["firstname"],
    "ln" : request.form["lastname"],
    "em" : request.form["email"],
    "pw" : request.form["password"],
    "pw_cnf" : request.form["password_confirm"],
    }
    err = []
    if len(data['fn']) < 2:
        err.append("First name needs to be at least 2 characters")
    if len(data['ln']) < 2:
        err.append("Username needs to be at least 2 characters")
    if not EMAIL_REGEX.match(data['em']):
        err.append("Email address is invalid")
    if len(data['pw']) < 8:
        err.append("Password needs to be at least 8 characters")
    if not data['pw'] == data['pw_cnf']:
        err.append("Passwords don't match")
    if len(err) > 0:
        for i in err:
            flash(i)
    else:
        data['pw'] = bcrypt.generate_password_hash(data['pw'])
        query = "INSERT INTO users (first_name, last_name, email_address, password_hash) VALUES ( %(fn)s, %(ln)s, %(em)s, %(pw)s )"
        query_result = mysql.query_db(query, data)
        session['firstname'] = data["fn"]
        session['uid'] = query_result
        return redirect('/jobs')

    return redirect('/')

@app.route('/login', methods=["post"])
def login():
    mysql = connectToMySQL('handy_helper')

    query = "SELECT * FROM users WHERE email_address = %(email)s;"
    data = { "email" : request.form['email'], "password" : request.form['password']}
    print(data)
    result = mysql.query_db(query, data)
    if result:
        if bcrypt.check_password_hash(result[0]['password_hash'], request.form['password']):
            session['uid'] = result[0]['id']
            session['firstname'] = result[0]["first_name"]
            return redirect('/jobs')

    flash("Login failed. Please check your credentials.")
    return redirect('/')

@app.route('/log_out')
def log_out():
    print("logging out...")
    session.clear()
    return redirect('/')

@app.route('/jobs')
def logged_in():
    if not 'uid' in session:
        return redirect('/')
    mysql = connectToMySQL('handy_helper')
    query = "SELECT * FROM jobs;"
    jobs = mysql.query_db(query)

    return render_template("jobs.html", all_jobs=jobs)

@app.route('/jobs/new')
def new_job():
    if not 'uid' in session:
        return redirect('/')
    return render_template('new_job.html')

@app.route('/create_job', methods = ["post"])
def create_job():
    if not 'uid' in session:
        return redirect('/')
    mysql=connectToMySQL('handy_helper')
    data = {
    "title" : request.form["title"],
    "desc" : request.form["description"],
    "loc" : request.form["location"],
    "post_by" : session['uid'],
    }
    err = []
    if len(data['title']) < 3:
        err.append("Job title must consist of at least 3 characters")
    if len(data['desc']) < 3:
        err.append("Description must consist of at least 3 characters")
    if len(data['loc']) < 3:
        err.append("Location must consist of at least 3 characters")
    if len(err) > 0:
        for i in err:
            flash(i)
    else:
        query = "INSERT INTO jobs (title, description, location, posted_by, created_at, updated_at) VALUES ( %(title)s, %(desc)s, %(loc)s, %(post_by)s, NOW(), NOW() )"
        mysql.query_db(query, data)
        return redirect('/jobs')

    return redirect('/jobs/new')

@app.route('/jobs/remove_job/<jobid>')
def remove_job(jobid):
    if not 'uid' in session:
        return redirect('/')
    mysql=connectToMySQL('handy_helper')
    data = { "job" : int(jobid) }
    query = "DELETE FROM jobs WHERE jobs.id = %(job)s"
    mysql.query_db(query, data)
    return redirect('/jobs')

@app.route('/jobs/edit/<jobid>')
def edit_job(jobid):
    if not 'uid' in session:
        return redirect('/')
    mysql=connectToMySQL('handy_helper')
    query = 'SELECT jobs.*, handy_helper.users.first_name, handy_helper.users.last_name FROM handy_helper.users JOIN handy_helper.jobs ON handy_helper.jobs.posted_by = handy_helper.users.id WHERE handy_helper.users.id = %(x)s'
    data = { "x" : int(jobid) }
    job_viewing = mysql.query_db(query,data)

    return render_template("edit_job.html", job=job_viewing)

@app.route('/edit_job/<jobid>', methods=['post'])
def edit_job_final(jobid):
    if not 'uid' in session:
        return redirect('/')
    mysql=connectToMySQL('handy_helper')
    data = {
    "title" : request.form["title"],
    "desc" : request.form["description"],
    "loc" : request.form["location"],
    "job" : int(jobid)
    }
    err = []
    if len(data['title']) < 3:
        err.append("Job title must consist of at least 3 characters")
    if len(data['desc']) < 3:
        err.append("Description must consist of at least 3 characters")
    if len(data['loc']) < 3:
        err.append("Location must consist of at least 3 characters")
    if len(err) > 0:
        for i in err:
            flash(i)
    else:
        query = "UPDATE jobs SET title = %(title)s, description = %(desc)s, location = %(loc)s, updated_at = NOW() WHERE id = %(job)s"
        mysql.query_db(query, data)
        return redirect('/jobs/'+jobid)
    return redirect('/jobs')

@app.route('/jobs/')
def invalid_jobs():
    if not 'uid' in session:
        return redirect('/')
    return redirect('/jobs')

@app.route('/jobs/<jobid>')
def view_job(jobid):
    if not 'uid' in session:
        return redirect('/')
    mysql = connectToMySQL('handy_helper')
    query = 'SELECT jobs.*, handy_helper.users.first_name, handy_helper.users.last_name FROM handy_helper.users JOIN handy_helper.jobs ON handy_helper.jobs.posted_by = handy_helper.users.id WHERE handy_helper.jobs.id = %(x)s'
    data = { "x" : int(jobid) }
    job_viewing = mysql.query_db(query,data)
    if job_viewing == False:
        return redirect('/jobs')
    return render_template('view_job.html', job=job_viewing)

@app.route('/jobs/add/<jobid>')
def add_job(jobid):
    if not 'uid' in session:
        return redirect('/')
    mysql=connectToMySQL('handy_helper')
    query = 'UPDATE jobs SET claimed_by = %(uid)s  WHERE id = %(job)s'
    data = { "job" : int(jobid), "uid" : session['uid'] }
    mysql.query_db(query, data)
    return redirect('/jobs')

@app.route('/jobs/giveup/<jobid>')
def give_up_job(jobid):
    if not 'uid' in session:
        return redirect('/')
    mysql=connectToMySQL('handy_helper')
    query = 'UPDATE jobs SET claimed_by = null  WHERE id = %(job)s'
    data = { "job" : int(jobid) }
    mysql.query_db(query, data)
    return redirect('/jobs')

if __name__ == "__main__":
    app.run(debug=True)
