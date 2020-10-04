import MySQLdb
import datetime

db = MySQLdb.connect('localhost','username', 'password', 'CAFE')
cursor = db.cursor()


cursor.execute("""SELECT MAX(STAFF_ID) FROM STAFF;""")
resp = cursor.fetchone()
if resp[0] is None:
	staffID = 1
staffID = resp[0] + 1

cursor.execute("""SELECT MAX(FOOD_ID) FROM MENU;""")
resp = cursor.fetchone()
if resp[0] is None:
	foodID = 1;
foodID = resp[0] + 1

cursor.execute("""SELECT MAX(CUSTOMER_ID) FROM CUSTOMER;""")
resp = cursor.fetchone()
if resp[0] is None:
	customerID = 1;
else:
	customerID = resp[0] + 1

cursor.execute("""SELECT MAX(ORDER_ID) FROM `ORDER`;""")
resp = cursor.fetchone()
if resp[0] is None:
	orderID = 1
else:
	orderID = resp[0] + 1

cursor.execute("""SELECT MAX(PAYMENT_ID) FROM PAYMENT;""")
resp = cursor.fetchone()
if resp[0] is None:
	paymentID = 1
else:
	paymentID = resp[0] + 1

def AddStaff():
	global staffID
	try:
		Fname = raw_input('Enter first name of employee: ')
		Lname = raw_input('Enter last name of employee: ')
		Email = raw_input('Enter email id of emlpoyee')
		address = raw_input('Enter address of employee')
		dob = raw_input('Enter Date of Birth of employee')
		staffCat = int(raw_input('Enter employee type (0 for chef, 1 for waiter, 2 for manager): '))
		tp = raw_input('Enter number of contact numbers you want to save for this employee')
		for i in tp:
			contactNumber = raw_input(i+': ')
			if len(contactNumber) != 10:
				print ("\nInvalid contact number")
				return
			contactNumber = int(contactNumber)
			mySql_insert_query = """INSERT INTO STAFF_CONTACT (STAFF_ID, CONTACT_NUMBER) VALUES (%s, %s)"""
			cursor.execute(mySql_insert_query, (staffID,contactNumber ))
			db.commit()


		if staffCat != 0 and staffCat != 1 and staffCat != 2:
			print ('\nInvalid employee type')
			return 
	except:
		print ("Invalid input(s)")
		return

	try:		
		mySql_insert_query = """INSERT INTO EMPLOYEES (STAFF_ID, FNAME, LNAME, EMAIL, ADDRESS, DOB, CATEGORY) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
		cursor.execute(mySql_insert_query, (staffID, Fname, Lname, Email, address, dob, staffCat))
		db.commit()
		# cursor.close()
		staffID = staffID + 1	
	
	except :
		print ("Error")
		db.rollback()

	try:
		# cursor = db.cursor()
		if staffCat == 0:
			WorkExp = raw_input('Enter work experience in years of the chef: ')
			mySql_insert_query = """INSERT INTO CHEF (STAFF_ID, WORK_EXPERIENCE) VALUES (%s, %s)"""
			cursor.execute(mySql_insert_query, (staffID - 1, WorkExp))
		elif staffCat == 1:
			ProfLang = raw_input('Enter the Proficient Language of the waitor: ')
			mySql_insert_query = """INSERT INTO WAITER (STAFF_ID, LANGUAGE) VALUES (%s, %s)"""
			cursor.execute(mySql_insert_query, (staffID - 1, ProfLang))
		db.commit()			
		# cursor.close()

	except:
		print ("Error")
		db.rollback()


def deleteStaff():
	try:
		empID = int(raw_input('Enter Staff ID of the staff you want to fire: '))
	except:
		print ("Invalid input")
		return
	cursor.execute("""SELECT * from STAFF WHERE STAFF_ID = %s;""", (empID,))
	rowcount = cursor.rowcount
	if rowcount == 0:
		print ('\nInvalid employee ID')
		return

	try:
		cursor.execute("""SELECT * from CHEF WHERE STAFF_ID = %s;""", (empID,))
		rowcount = cursor.rowcount
		if rowcount !=0:
			resp = cursor.fetchone()
			# if resp[1] is not None:
			# 	print ('Cannot fire employee as the employee is working on an order')
			# 	return
			cursor.execute("""DELETE from CHEF WHERE STAFF_ID = %s;""", (empID,))
			cursor.execute("""DELETE from STAFF WHERE STAFF_ID = %s;""", (empID,))
			db.commit()

		cursor.execute("""SELECT * from WAITER WHERE STAFF_ID = %s;""", (empID,))
		rowcount = cursor.rowcount

		if rowcount !=0:
			cursor.execute("""SELECT * from WAITER WHERE STAFF_ID = %s;""", (empID,))
			resp = cursor.fetchone()
			# if resp[1] is not None:
			# 	print ('Cannot fire employee as the employee is working on an order')
			# 	return
			cursor.execute("""DELETE from WAITER WHERE STAFF_ID = %s;""", (empID,))
			cursor.execute("""DELETE from STAFF WHERE STAFF_ID = %s;""", (empID,))
			db.commit()
	except:
		print ("Error!")
		return
	return

def addMenu():
	global foodID
	# db = MySQLdb.connect('localhost','root', '12345678', 'RESTAURANT')
	item=raw_input("Enter the name of food item: ")
	
	# cursor = db.cursor()
	cursor.execute("""SELECT COUNT(*) FROM MENU WHERE NAME = %s;""",(item,))
	exists = cursor.fetchone()
	# cursor.close()
	if exists[0] != 0:
		print
		print ("Item already exists")
		return
	
	try:
		about = raw_input("Enter about the food item: ")
		foodCat = raw_input("Enter the type of food item: ")
		price=float(raw_input("Enter its price: "))
	except:
		print ("Invalid input")
		return
	
	try:
		# cursor = db.cursor()
		cursor.execute("""INSERT INTO MENU VALUES (%s,%s,%s,%s,%s,%s);""",(foodID,item,about,price,0,0))
		cursor.execute("""INSERT INTO FOOD_CATEGORY VALUES (%s,%s);""",(foodID,foodCat))
		db.commit()
		print ("added new menu item")
		foodID=foodID+1
		# cursor.close()
	except:
		db.rollback()
	# db.close()


def changePrice():
	# db = MySQLdb.connect('localhost','root', '12345678', 'RESTAURANT')
	item =  raw_input('Enter name of item whose price you want to change: ')
	# cursor = db.cursor()
	cursor.execute("""SELECT COUNT(*) FROM MENU WHERE NAME = %s;""",(item,))
	exists = cursor.fetchone()
	if exists[0] == 0:
		print ("\nItem does not exist in the Menu")
		return

	try:
		price = int(raw_input('Enter new price: '))
	except:
		print ("Invalid input")
		return

	try:	
		cursor.execute("""UPDATE MENU SET PRICE = %s WHERE NAME = %s;""", (price, item,))
		db.commit()
		print
		print ("Price changed")

	except:
		print ("Error")
		db.rollback()


def removeitem():

	item = raw_input('Enter name of the item you want to remove from menu')

	try:
		cursor.execute("""SELECT COUNT(*) FROM MENU WHERE FOOD_ITEM = %s;""",(item,))
		exists = cursor.fetchone()

		if exists[0] == 0 :
			print
			print "Item does not exist in the Menu"
			return

		cursor.execute("""DELETE FROM MENU WHERE FOOD_ITEM = %s;""",(item,))
		db.commit()
		# cursor.close()
		print
		print "Item deleted from Menu"
	
	except:
		print "Error"
		db.rollback()
		
	# cursor.close()
	# db.close()

def addCustomer():
	global customerID
	# db = MySQLdb.connect('localhost','root', '12345678', 'RESTAURANT')
	# cursor = db.cursor()

	# cursor.execute("""SELECT * FROM `CUSTOMER` WHERE CUSTOMER_ID = %s;""",(customerID))
	# rowcount = cursor.rowcount
	# if rowcount != 0:
	# 	print
	# 	print ("Cannot add a new customer as no table is free")
	# 	return
	
	Fname = raw_input('Enter first name of customer: ')
	Lname = raw_input('Enter last name of customer: ')
	contactNo = raw_input('Enter contact number of customer: ')

	# table = cursor.fetchone()
	try:	
		mySql_insert_query = """INSERT INTO CUSTOMER (CUSTOMER_ID, FNAME, LNAME, CONTACT_NUMBER) VALUES (%s, %s, %s, %s)"""
		cursor.execute(mySql_insert_query, (customerID, Fname, Lname, contactNo))
		db.commit()
		customerID = customerID + 1

	except:
		print ("Error")
		db.rollback()

	# cursor.close()
	# db.close()


def updateCustomer():
	# db = MySQLdb.connect('localhost','root', '12345678', 'RESTAURANT')
	# cursor = db.cursor()
	custid =  raw_input('Enter Customer ID whose details you want to change: ')
	cursor.execute("""SELECT * FROM `CUSTOMER` WHERE CUSTOMER_ID = %s;""",(custid))
	rowcount = cursor.rowcount
	if rowcount == 0:
		print
		print ("No customer with this id")
		return
	
	contactNo = raw_input('Enter new contact number of customer: ')

	# table = cursor.fetchone()
	try:
		cursor.execute("""UPDATE CUSTOMER SET CONTACT_NUMER = %s,  WHERE CUSTOMER_ID = %s;""", (contactNo, custid,))	
		db.commit()

	except:
		print ("Error")
		db.rollback()

	# cursor.close()
	# db.close()

def calcSalary():
	staff_id = raw_input('Enter STAFF_ID whose total salary you want to know: ')
	cursor.execute("""SELECT * FROM `SALARY` WHERE STAFF_ID = %s;""",(staff_id))
	rowcount = cursor.rowcount
	if rowcount == 0:
		print
		print ("No staff with this id")
		return

	response = cursor.fetchone()
	totsal = response[1] + response[2] - response[3];
	print("\n Total Salary = " + totsal)


def calcAvgRating():
	food_name = raw_input('Enter Name of food item whose rating you want to know: ')
	cursor.execute("""SELECT * FROM `MENU` WHERE NAME = %s;""",(food_name))
	rowcount = cursor.rowcount
	if rowcount == 0:
		print
		print ("No food with this name")
		return

	response = cursor.fetchone()
	print("\n Rating = " + (response[5]/response[4]))


def addStaffDependent():
	try:
		stid=int(raw_input("Enter the staff id: "))
	except:
		print ("Invalid input")
		return

	cursor.execute("""SELECT * FROM STAFF WHERE STAFF_ID = %s;""",(stid,))
	rowcount = cursor.rowcount
	if rowcount == 0:
		print ("Invalid employee id")
		return

	emp = cursor.fetchone()
	edfname = raw_input("Enter associate's first name: ")
	edlname = raw_input("Enter associate's last name: ")
	edadd = raw_input("Enter associate's address: ")
	edcno = raw_input("Enter associate's last name: ")
	try:
		cursor.execute("""SELECT * FROM STAFF_ASSOCIATES WHERE STAFF_ID = %s AND FNAME = %s AND LNAME = %s;""",(stid,edfname,edlname))
		rowcount = cursor.rowcount
		if rowcount != 0:
			print ("Dependent information already present")
			return

		mySql_insert_query = """INSERT INTO STAFF_ASSOCIATE (STAFF_ID, FNAME, LNAME, ADDRESS, CONTACT_NUMBER) VALUES (%s,%s,%s,%s,%s);"""
		cursor.execute(mySql_insert_query,(stid,edfname,edlname,edadd,edcno))
		db.commit()
	except :
		print ("Error")
		db.rollback()

