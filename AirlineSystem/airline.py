from flask import Flask,render_template,request
import sqlite3 as sql

app=Flask(__name__)

#Homepage
@app.route('/')
def home():
    return render_template('home.html')

#SignUp
@app.route('/signUp',methods=['GET','POST'])
def signUp():
    if (request.method=='GET'):
        return render_template('signUp.html')

#SignUp after Submission
@app.route('/successRegistration',methods=['GET','POST'])
def successRegistration():
    if(request.method=='POST'):
        try:
            name=request.form['name']
            email=request.form['email']
            passwd=request.form['passwd']
            phone=request.form['phone']
            gender=request.form['formRadio']
            with sql.connect("database.db") as con:
                cur=con.cursor()
                cur.execute("INSERT OR IGNORE INTO Users(user_id,email,password,phone_number,gender)VALUES(?,?,?,?,?)",(name,email,passwd,phone,gender))
                con.commit()
                msg="Insertion Successful"
        except:
            con.rollback()
            msg="Error in Insertion"
        finally:
            return render_template('successRegistration.html',msg=msg)
            con.close()

#Login
@app.route('/login',methods=['GET','POST'])
def login():
    if(request.method=='GET'):
        return render_template('login.html')

#After Login Userbook random checking pr
@app.route('/userBook',methods=['GET','POST'])
def userBook():
    if(request.method=='POST'):
        name=request.form['name']
        passwd=request.form['passwd']
        con=sql.connect("database.db")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("SELECT * FROM Users WHERE user_id=?",(name,))
        rows=cur.fetchall()
        var=str(rows[0]['email'])
        if(rows):
            password=rows[0][2]
            if(passwd == password):
                return render_template('userBook.html',var=var)
            else:
                msg="Error in Password"
                return render_template("login.html",msg=msg)
        else:
            msg="No Such User Exists"
            return render_template('login.html',msg=msg)

#Query Flight
@app.route('/flight_details',methods=['GET','POST'])
def flight_details():
    if(request.method=='POST'):
        source=request.form['source']
        dest=request.form['dest']
        date=request.form['date']
        con=sql.connect("database.db")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("SELECT * FROM Airlines where source=? AND destination=? AND date=?",(source,dest,date,))
        rows=cur.fetchall()
        if(rows):
            return render_template('showFlights.html',rows=rows)
        else:
            msg="No Such Flights Present On This Date"
            return render_template('userBook.html',msg=msg)

#Flight Details
@app.route('/calculatePrice/<flight_number>',methods=['GET','POST'])
def calculatePrice(flight_number):
    if(request.method=='GET'):
        return render_template('showBooking.html',flight_number=flight_number)

#Show Bookings
@app.route('/passenger_details/<flight_number>',methods=['GET','POST'])
def passenger_details(flight_number):
    if(request.method=='POST'):
        name=request.form['name']
        phone=request.form['phone']
        email=request.form['email']
        con=sql.connect("database.db")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("SELECT * FROM Airlines where flight_number=?",(flight_number,))
        rows=cur.fetchall()
        return render_template('showDetails.html',rows=rows,name=name,phone=phone,email=email,flight_number=flight_number)

#Confirm Booking
@app.route('/confirm_booking/<email>/<flight_number>',methods=['GET','POST'])
def confirm_booking(email,flight_number):
    try:
        with sql.connect("database.db") as con:
            cur=con.cursor()
            cur.execute("INSERT OR IGNORE INTO Bookings(email,flight_num)VALUES(?,?)",(email,flight_number))
            con.commit()
            msg="Booking Confirmed"
    except:
        con.rollback()
        msg="Not Booked"
    finally:
        return render_template('successRegistration.html',msg=msg)
        con.close()

#Show Older Booking
@app.route('/showOlderBooking/<email>',methods=['GET','POST'])
def showOlderBooking(email):
    if(request.method=='GET'):
        con=sql.connect("database.db")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("SELECT * FROM Bookings where email=?",(email,))
        rows=cur.fetchall()
        return render_template('showOlderBookings.html',rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
