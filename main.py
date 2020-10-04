import MySQLdb
import datetime

db = MySQLdb.connect('localhost','DAproject', '$onofaguN77', 'CAFE')
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

cursor.execute("""SELECT MAX(ORDER_ID) FROM `ORDERS`;""")
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

cursor.execute("""SELECT MAX(INVOICE_ID) FROM COMPLETE_INFO;""")
resp = cursor.fetchone()
if resp[0] is None:
	invoiceID = 1
else:
	invoiceID = resp[0] + 1

def addStaff():
	global staffID
	try:
		Fname = raw_input('Enter first name of employee: ')
		Lname = raw_input('Enter last name of employee: ')
		email = raw_input('Enter email of employee: ')
		address = raw_input('Enter address of employee: ')
		dob = raw_input('Enter DOB of employee: ')

		employeeType = int(raw_input('Enter employee type (0 for chef, 1 for waiter, 2 for manager): '))
		if employeeType != 0 and employeeType != 1 and employeeType !=  2:
			print 
			print ('Invalid employee type')
			print
			return

		mySql_insert_query = """INSERT INTO STAFF (STAFF_ID, FNAME, LNAME, EMAIL, ADDRESS, DOB, CATEGORY ) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
		cursor.execute(mySql_insert_query, (staffID, Fname, Lname, email, address, dob, employeeType))
		db.commit()

		if employeeType == 0:
			wexp = int(raw_input('Enter WORK EXPERIENCE of chef in years: '))
			mySql_insert_query = """INSERT INTO CHEF (STAFF_ID, WORK_EXPERIENCE) VALUES (%s, %s)"""
			cursor.execute(mySql_insert_query, (staffID - 1, wexp))
		elif employeeType == 1:
			proflang = raw_input('Enter proficient language of waitor in years: ')
			mySql_insert_query = """INSERT INTO WAITER (STAFF_ID, LANGUAGE) VALUES (%s, %s)"""
			cursor.execute(mySql_insert_query, (staffID - 1, proflang))
		db.commit()

		while(1): 
			contactNumber = raw_input('Enter contact number of employee: ')
			if len(contactNumber) != 10:
				print 
				print ("Invalid contact number")
				return
			contactNumber = int(contactNumber)
			mySql_insert_query = """INSERT INTO STAFF_CONTACT (STAFF_ID, CONTACT_NUMBER ) VALUES (%s, %s)"""
			cursor.execute(mySql_insert_query, (staffID, contactNumber))
			db.commit()
			ch = raw_input("Enter Another contact number? (Y-Yes / N-No) : ")
			if ch == 'N' or ch == 'n' or ch == 'no' or ch == 'No' or ch == 'NO':
				break
		staffID = staffID + 1	
		print("Added Staff!!")
	except :
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
			cursor.execute("""DELETE from CHEF WHERE STAFF_ID = %s;""", (empID,))
			cursor.execute("""DELETE from STAFF WHERE STAFF_ID = %s;""", (empID,))
			db.commit()

		cursor.execute("""SELECT * from WAITER WHERE STAFF_ID = %s;""", (empID,))
		rowcount = cursor.rowcount

		if rowcount !=0:
			cursor.execute("""SELECT * from WAITER WHERE STAFF_ID = %s;""", (empID,))
			resp = cursor.fetchone()
			cursor.execute("""DELETE from WAITER WHERE STAFF_ID = %s;""", (empID,))
			cursor.execute("""DELETE from STAFF WHERE STAFF_ID = %s;""", (empID,))
			db.commit()
		print("Fired Staff!!")
	except:
		print ("Error!")
		return

def addMenu():
	global foodID
	item=raw_input("Enter the name of food item: ")
	
	cursor.execute("""SELECT COUNT(*) FROM MENU WHERE NAME = %s;""",(item,))
	exists = cursor.fetchone()
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
		cursor.execute("""INSERT INTO MENU VALUES (%s,%s,%s,%s,%s,%s);""",(foodID,item,about,price,0,0))
		cursor.execute("""INSERT INTO FOOD_CATEGORY VALUES (%s,%s);""",(foodID,foodCat))
		db.commit()
		print ("Added new menu item")
		foodID=foodID+1
	except:
		db.rollback()
	# db.close()

# def deleteMenu():
# 	try:
# 		food_ID = int(raw_input('Enter Food ID of the item you want to remove: '))
# 	except:
# 		print ("Invalid input")
# 		return
# 	cursor.execute("""SELECT * from MENU WHERE FOOD_ID = %s;""", (food_ID,))
# 	rowcount = cursor.rowcount
# 	if rowcount == 0:
# 		print ('\nInvalid food ID')
# 		return

# 	resp = cursor.fetchone()
# 	cursor.execute("""DELETE from MENU WHERE FOOD_ID = %s;""", (food_ID,))
# 	db.commit()

# 	print("REMOVED \n")
# 	print ("Error!")

def changePrice():
	item =  raw_input('Enter name of item whose price you want to change: ')
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

	# cursor.close()
	# db.close()

def addCustomer():
	global customerID
	Fname = raw_input('Enter first name of customer: ')
	Lname = raw_input('Enter last name of customer: ')
	contactNo = int(raw_input('Enter contact number of customer: '))

	# table = cursor.fetchone()
	try:	
		mySql_insert_query = """INSERT INTO CUSTOMER (CUSTOMER_ID, FNAME, LNAME, CONTACT_NUMBER) VALUES (%s, %s, %s, %s)"""
		cursor.execute(mySql_insert_query, (customerID, Fname, Lname, contactNo))
		db.commit()
		customerID = customerID + 1
		print("Added!!")
	except:
		print ("Error")
		db.rollback()

def updateCustomer():

	custid =  int(raw_input('Enter Customer ID whose details you want to change: '))
	try:
		cursor.execute("""SELECT * FROM `CUSTOMER` WHERE CUSTOMER_ID = %s;""",(custid,))
		rowcount = cursor.rowcount
		if rowcount == 0:
			print
			print ("No customer with this id")
			return
		
		contactNo = int(raw_input('Enter new contact number of customer: '))

		cursor.execute("""UPDATE CUSTOMER SET CONTACT_NUMBER = %s WHERE CUSTOMER_ID = %s;""", (contactNo, custid,))	
		db.commit()
		print("Updated!!")
	except:
		print ("Error")
		db.rollback()

def calcSalary():
	staff_id = raw_input('Enter STAFF_ID whose total salary you want to know: ')
	cursor.execute("""SELECT * FROM `SALARY` WHERE STAFF_ID = %s;""",(staff_id,))
	rowcount = cursor.rowcount
	if rowcount == 0:
		print
		print ("No staff with this id")
		return

	response = cursor.fetchone()
	totsal = response[1] + response[2] - response[3];
	print("\n Total Salary = " + str(totsal))


def calcAvgRating():
	try:
		food_name = raw_input('Enter Name of food item whose rating you want to know: ')
		cursor.execute("""SELECT * FROM MENU WHERE NAME = %s;""",(food_name,))
		rowcount = cursor.rowcount
		if rowcount == 0:
			print
			print ("No food with this name")
			return
		response = cursor.fetchone()
		print("\n Rating = " + str(response[5]/response[4]))
	except:
		print ("Error")
		db.rollback()


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
	edcno = int(raw_input("Enter associate's contact no: "))
	try:
		cursor.execute("""SELECT * FROM STAFF_ASSOCIATES WHERE STAFF_ID = %s AND FNAME = %s AND LNAME = %s;""",(stid,edfname,edlname))
		rowcount = cursor.rowcount
		if rowcount != 0:
			print ("Dependent information already present")
			return

		mySql_insert_query = """INSERT INTO STAFF_ASSOCIATES (STAFF_ID, FNAME, LNAME, ADDRESS, CONTACT_NUMBER) VALUES (%s,%s,%s,%s,%s);"""
		cursor.execute(mySql_insert_query,(stid,edfname,edlname,edadd,edcno))
		db.commit()
		print("Added!!")
	except :
		print ("Error")
		db.rollback()


def searchFoodByName():
	try:
		foodname = raw_input("Enter the name of the food item you want to know about: ")
		cursor.execute("""SELECT * FROM MENU WHERE NAME = %s;""",(foodname,))
		rowcount = cursor.rowcount
		if rowcount == 0:
			print ("\nNo such food item.")
			return
		foodresp = cursor.fetchall()
		for response in foodresp:
			print("\nFOOD_ID = "+ str(response[0]))
			print("\nABOUT = "+ response[2])
			print("\nPRICE = "+ str(response[3]))
			print("\nAVG RATING = "+ str(response[5]/response[4]))
	except:
		print ("Error")
		db.rollback()

def searchFoodByCategory():
	try:
		foodcat = raw_input("Enter the category of the food item you want to know about: ")
		cursor.execute("""SELECT * FROM FOOD_CATEGORY WHERE  CATEGORY = %s;""",(foodcat,))
		rowcount = cursor.rowcount
		if rowcount == 0:
			print ("\nNo food item of this category.")
			return
		foodresp = cursor.fetchall()
		for response in foodresp:
			cursor.execute("""SELECT * FROM MENU WHERE FOOD_ID = %s;""",(response[0],))
			foodname = cursor.fetchone()
			print(foodname[1]+"\n")
			print
	except:
		print("Error")
		db.rollback

def placeOrder():
	global orderID
	global paymentID
	global invoiceID
	custoption = int(raw_input('Customer already a member or not? (1 for yes, 2 for no)'))

	if custoption == 2:
		addCustomer()

	try:
		custID = int(raw_input('Enter customer ID: '))
	except:
		print ("Invalid input")
		return


	cursor.execute("""SELECT * FROM CUSTOMER WHERE CUSTOMER_ID = %s;""", (custID,))
	rowcount = cursor.rowcount
	if rowcount == 0:
		print
		print ("Invalid customerID")
		return

	customer = cursor.fetchone()
	
	tabnum = int(raw_input("Enter table number : "))
	nowtime = datetime.datetime.now()
	nowtime = nowtime.strftime("%H:%M:%S")
	mySql_insert_query = """INSERT INTO COMPLETE_INFO (INVOICE_ID, CUSTOMER_ID, TABLE_NUMBER, TIME_OF_DAY, TOTAL_AMOUNT, STATUS) VALUES (%s,%s,%s,%s,%s,%s);"""
	cursor.execute(mySql_insert_query,(invoiceID, customer[0], tabnum, nowtime, 0, "PENDING"))
	db.commit()
	totamt = 0;
	while True:
		try:
			food_name  = raw_input("Enter name of food item: ")
			quantity = int(raw_input('Enter its quantity: '))
			discnt = int(raw_input('Enter discount: '))
		except:
			print ("Invalid input")
			return
		
		cursor.execute("""SELECT * FROM MENU WHERE NAME = %s;""", (food_name,))
		rowcount = cursor.rowcount
		if rowcount == 0:
			print
			print ("Invalid name")
			return
		
		food_resp = cursor.fetchone()
		cursor.execute("""SELECT * FROM CHEF ORDER BY RAND() LIMIT 1;""")
		chef_resp = cursor.fetchone()
		foodid = int(food_resp[0])
		chefid = int(chef_resp[0])
		rating = 5

		mySql_insert_query = """INSERT INTO ORDERS (ORDER_ID, INVOICE_ID, FOOD_ID, STAFF_ID, DISCOUNT, QUANTITY, RATING) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
		cursor.execute(mySql_insert_query, (orderID, invoiceID, foodid, chefid, discnt, quantity, rating))
		db.commit()

		cursor.execute("""SELECT * FROM WAITER ORDER BY RAND() LIMIT 1;""")
		waiter_resp = cursor.fetchone()

		mySql_insert_query = """INSERT INTO ORDERING (CUSTOMER_ID, ORDER_ID) VALUES (%s,%s);"""
		cursor.execute(mySql_insert_query,(customer[0],orderID))
		db.commit()
		
		mySql_insert_query = """INSERT INTO SERVING (STAFF_ID, ORDER_ID) VALUES (%s,%s);"""
		cursor.execute(mySql_insert_query,(waiter_resp[0],orderID))
		db.commit()

		mySql_insert_query = """INSERT INTO PREPARING (STAFF_ID, ORDER_ID) VALUES (%s,%s);"""
		cursor.execute(mySql_insert_query,(chef_resp[0],orderID))
		db.commit()

		orderID = orderID + 1
		totamt = totamt + int(food_resp[3])

		rateOrder(food_resp[1], quantity)

		flag = raw_input(("Finish Ordering? (enter Y for Yes, N for No)"))	
		if flag == 'Y' or flag == 'y':
			break;

	cursor.execute("""UPDATE COMPLETE_INFO SET TOTAL_AMOUNT = %s WHERE INVOICE_ID = %s;""", (totamt, invoiceID,))
	db.commit()
	invoiceID = invoiceID + 1;

	print("Thank you for ordering!!")


def makePayment():
	invID = int(raw_input("Enter the Invoice ID: "))
	try: 
		cursor.execute("""SELECT * FROM COMPLETE_INFO WHERE INVOICE_ID = %s;""", (invID,))
		rowcount = cursor.rowcount
		if rowcount == 0:
			print ("\nInvalid invoice ID")
			return
		invresp = cursor.fetchone()

		portal = raw_input("Enter Portal (CASH / CREDIT CARD / DEBIT CARD / PAYTM / GPAY / AMAZON PAY / OTHERS) : ")
		mySql_insert_query = """INSERT INTO PAYMENT (PAYMENT_ID, INVOICE_ID, AMOUNT, PORTAL) VALUES (%s,%s,%s,%s);"""
		cursor.execute(mySql_insert_query,(paymentID,invID, invresp[4],portal))
		db.commit()
		print
		cursor.execute("""UPDATE COMPLETE_INFO SET STATUS = %s WHERE INVOICE_ID = %s;""", ('PAID', invID,))
		db.commit()

		print("\nPAID\n")
	except:
		print("Error")
		db.rollback

def rateOrder(foodname, quantity):
	# foodname = int(raw_input("Enter food name you want to rate : "))
	print("Rate this item: \n")
	cursor.execute("""SELECT * FROM MENU WHERE NAME = %s;""",(foodname,))
	rowcount = cursor.rowcount
	if rowcount == 0:
		print ("\nNo such food item.")
		return
	foodresp = cursor.fetchone()

	stars = int(raw_input("Enter number of stars: (1 or 2 or 3 or 4 or 5) : "))
	if stars > 5 or stars < 1:
		print("Invalid rating")
		return

	totrating = foodresp[5] + stars

	cursor.execute("""UPDATE MENU SET RATING = %s , NO_OF_TIMES_ORDERED = %s WHERE NAME = %s;""", (totrating, foodresp[4]+quantity, foodname,))
	db.commit()
	return

def showMostOrdered():
	cursor.execute("""SELECT MAX(NO_OF_TIMES_ORDERED) FROM MENU;""")
	number = cursor.fetchone()
	cursor.execute("""SELECT NAME FROM MENU WHERE NO_OF_TIMES_ORDERED = %s;""", (number,))
	items = cursor.fetchall()

	for i in items:
		print(str(i[0])+"\n")

def rateOrder():
	foodname = raw_input("Enter food name you want to rate : ")
	print("Rate this item: \n")
	cursor.execute("""SELECT * FROM MENU WHERE NAME = %s;""",(foodname,))
	rowcount = cursor.rowcount
	if rowcount == 0:
		print ("\nNo such food item.")
		return
	foodresp = cursor.fetchone()

	stars = int(raw_input("Enter number of stars: (1 or 2 or 3 or 4 or 5) : "))
	if stars > 5 or stars < 1:
		print("Invalid rating")
		return

	totrating = foodresp[5] + stars

	cursor.execute("""UPDATE MENU SET RATING = %s , NO_OF_TIMES_ORDERED = %s WHERE NAME = %s;""", (totrating, foodresp[4]+1, foodname,))
	db.commit()
	return

def setManager():
	managerid = int(raw_input("Enter Manager - id : "))
	staff_id = int(raw_input("Enter Staff - id : "))
	# cursor.execute("""SELECT NAME FROM MENU WHERE NO_OF_TIMES_ORDERED = %s;""", (number,))

	cursor.execute("""SELECT STAFF_ID FROM STAFF WHERE STAFF_ID = %s AND CATEGORY = %s;""",(managerid,2,))
	rowcount = cursor.rowcount
	if rowcount == 0:
		print ("\nInvalid Manager ID.")
		return

	cursor.execute("""SELECT STAFF_ID FROM STAFF WHERE STAFF_ID = %s AND CATEGORY <> %s;""",(staff_id,2,))
	rowcount = cursor.rowcount
	if rowcount == 0:
		print ("\nInvalid Staff ID.")
		return

	mySql_insert_query = """INSERT INTO MANAGES (MANAGER_ID, STAFF_ID) VALUES (%s,%s);"""
	cursor.execute(mySql_insert_query,(managerid, staff_id))
	db.commit()

	print("Manager set!!")
		

while True:
	print("1: Add new Staff")
	print("2: Delete a Staff")
	print("3: Add new menu item")
	print("4: Rate Food Item")
	print("5: Place Order")
	print("6: Add new customer")
	print("7: Update custome details")
	print("8: Change Price of Food Item")
	print("9: See Average Rating of Food Item")
	print("10: Calculate Salary of Emloyee")
	print("11: Add Staff-Dependent Details")
	print("12: Search Food item by name")
	print("13: Search Food item by category")
	print("14: Make Payment")
	print("15: Show Most Ordered Item")
	print("16: Set Manager for staff")
	print("0: exit")
	choice = int(input("Enter your choice: "))

	if choice == 1:
		addStaff()
	
	elif choice == 2:
		deleteStaff()

	elif choice == 3:
		addMenu()

	elif choice == 4:
		rateOrder()

	elif choice == 5:
		placeOrder()

	elif choice == 6:
		addCustomer()

	elif choice == 7:
		updateCustomer()

	elif choice == 8:
		changePrice()

	elif choice == 9:
		calcAvgRating()

	elif choice == 10:
		calcSalary()

	elif choice == 11:
		addStaffDependent()

	elif choice == 12:
		searchFoodByName()

	elif choice == 13:
		searchFoodByCategory()

	elif choice == 14:
		makePayment()

	elif choice == 15:
		showMostOrdered()

	elif choice == 16:
		setManager()

	elif choice == 0:
		break


	else:
		print ("Enter a valid choice!!!")

	print ("---------------------------------------------------------------------------------------------------------------------------------------------")

cursor.close()
db.close()
print ('Hasta la\'vista')