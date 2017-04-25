from flask import Flask, render_template, json, request
#from flask.ext.mysql import MySQL
#from flask_mysql import MySQL
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
import sys

mysql = MySQL()
app = Flask(__name__)
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'Matthew'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Matthew123!@#'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)




@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


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


