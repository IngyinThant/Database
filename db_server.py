from flask import Flask, render_template, jsonify, request, flash
import sqlite3, json

app=Flask(__name__)

@app.route('/')
def indexPage():
	return render_template("db_student.html")

@app.route('/save', methods=['GET','POST'])
def saveStudent():
	print("saving student" + request.method)
	error=''
	if request.method =='POST':
		try:
			print(request.form)
			name=request.form['Name']
			phy=int(request.form['Physics'])
			che=int(request.form['Chemistry'])
			math=int(request.form['Maths'])
		except ValueError:
			error="data input error"
			return render_template("db_student.html", error=error)
		try:
			with sqlite3.connect("C:/Users/X541UJ/Lectures/student.db") as con:
				cur=con.cursor()
			cur.execute("insert into Student_List(Name,Physics,Chemistry,Maths) values(?,?,?,?)",(name,phy,che,math))
			con.commit()
			msg="saving"
			return redirect(url_for("Flash_message.html", msg=msg))

		except:
			con.rollback()
		finally:
			con.close()
			return render_template("db_student.html", error=error)
	return render_template("db_student.html", error=error)

@app.route('/allStudents')
def studentInformation():
	con= sqlite3.connect("C:/Users/X541UJ/Lectures/student.db")
	cur=con.cursor()
	cur.execute("select * from Student_List")
	rows=cur.fetchall()
	print(rows)
	return json.dumps(rows)


if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
