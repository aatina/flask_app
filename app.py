from flask import Flask, render_template, json, redirect, request, session
import hashlib
import MySQLdb
import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'
# mysql = MySQL()

# MySQL configurations
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
# app.config['MYSQL_DATABASE_DB'] = 'flaskapp'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)

### Pages ###
@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showSignIn')
def showSignin():
    return render_template('signin.html')

@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')

### Functions ###

# Creating new user
@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            # Connect to mySQL
            conn = pymysql.connect(host="localhost",
                     user="root",
                     passwd="password",
                     db="flaskapp")

            cursor = conn.cursor()
            _hexhash = hashlib.sha512(_password).hexdigest()
            cursor.callproc('sp_createUser',(_name,_email,_hexhash))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return render_template('error.html',error = str(e))
    # finally:
    #      conn.close()

# Login validate method
@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        # Connect to mySQL
        conn = pymysql.connect(host="localhost",
                    user="root",
                    passwd="password",
                    db="flaskapp")

        cursor = conn.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()

        # Check password and create a user session
        if len(data) > 0:
            if str(data[0][3]) == hashlib.sha512(_password).hexdigest():
                session['user'] = data[0][0]
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')

 
    except Exception as e:
        return render_template('error.html',error = str(e))
    # finally:
    #     conn.close()

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')


if __name__ == "__main__":
    app.run(host='0.0.0.0')