from flask import Flask, render_template, json, request,redirect,session
#from flask.ext.mysql import MySQL
#from flask_mysql import MySQL
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
import sys

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'
#app.run(debug = True)  #restarts server when changes detected.
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'Matthew'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Matthew123!@#'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)



@app.route("/")
def main():
    return render_template('index.html')

@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showSignin')
def showSignin():
	return render_template('signin.html')

@app.route('/logout')
def logout():
	session.pop('user',None)
	return redirect('/')#returns to route '/' above 


@app.route('/validateLogin',methods=['POST'])
def validateLogin():
	try:
		_username = request.form['inputEmail']
		_password = request.form['inputPassword']
 
		# connect to mysql
 
		con = mysql.connect()
		cursor = con.cursor()
		cursor.callproc('sp_validateLogin',(_username,))
		data = cursor.fetchall()
 
		if len(data) > 0:
			if check_password_hash(str(data[0][3]),_password):
				print('check_password_hash = True', file=sys.stderr)
				session['user'] = data[0][0]
				return redirect('/userHome')
			else:
				print('check_password_hash = False', file=sys.stderr)
				return render_template('error.html',error = 'Wrong Email address or Password.')
		else:
			print('len(data) !> 0', file=sys.stderr)
			return render_template('error.html',error = 'Wrong Email address or Password.')
 
 
	except Exception as e:
		print('Exception = '+str(e), file=sys.stderr)
		return render_template('error.html',error = str(e))
	finally:
		cursor.close()
		con.close()


@app.route('/signUp',methods=['POST'])
def signUp():
    # read the posted values from the UI
	_name = request.form['inputName']
	_email = request.form['inputEmail']
	_password = request.form['inputPassword']
	print("inputName = '"+_name+"', inputEmail = '"+_email+"', inputPassword = '"+_password+"'", file=sys.stderr)
 
    # validate the received values
    #NB: output from return json.dumps appears in browser console 
	if _name and _email and _password:
		conn = mysql.connect()
		#console.log("database connection initialized.")
		cursor = conn.cursor()
		#console.log("conn.cursor() = ", cursor)
		_hashed_password = generate_password_hash(_password)
		print("_hashed_password = '"+_hashed_password+"', length = "+str(len(_hashed_password)), file=sys.stderr)
		cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
		#cursor.callproc('sp_createUser',(_name,_email,_password))
		data = cursor.fetchall()
		if len(data) is 0:
			conn.commit()
			return json.dumps({'message':'User created successfully !'})
		else:
			return json.dumps({'error':str(data[0])})

	else:
		return json.dumps({'html':'<span>Enter the required fields</span>'})


if __name__ == "__main__":
    app.run()


