# MAIN_CODE:
import mysql.connector
db1 = None
def connect():
    global db1
    db1 = mysql.connector.connect(host="localhost",user="root",
    password="root",
    database = "shashwat"
  )
  

def showusers():
    c1 = db1.cursor()
    c1.execute("select * from vacine")
    res = c1.fetchall()
    #print(res)
    print("List of Users ")
    for val in res:
        print("UserName = "+val[0] + " Password = " + val[1])

def login():
    print("-" * 60)
    print("\t WELCOME TO COVID VACCINATION RECORDS ππ₯π§‘π―")
    print("-" * 60)
    import datetime
    now = datetime.datetime.now()
    print("Current Dateπ & Timeβ±οΈ:")
    print(now.strftime("%y/%m/%d & %H:%M:%S"))
    print("-" * 60)
    print("\t USER LOGIN INFO:π¦π₯")
    print("-" * 60)
    un = input("Enter User Name π€΄ π ")
    pw = input("Enter Password π π ")
    q = "select * from vacine where username = %s and passw = %s"
    val = (un,pw)
    c2 = db1.cursor()
    c2.execute(q,val)
    res = c2.fetchall()
    print("-" * 60)
    if len(res) == 0:
        print("Invalid User Name or Password β... ")
        print("Better Luck Next Time π€£ππ―")
        print("-" * 60)
        return False
    else:
        print("Access Granted !!!πππ€")
        print("-" * 60)
        return True
    
def addmember():
    ad = input("Enter Aadhar Card No. π ")
    name = input("Enter Member Name π ")
    addr = input("Enter Address π ")
    phone = input("Enter Phone Number π ")
    email = input("Enter Email π ")
    age = input("Enter Age of member π ")
    cursor1 = db1.cursor()
    q = "insert into member values (%s,%s,%s,%s,%s,%s)"
    val = (ad,name,addr,phone,email,age)
    cursor1.execute(q,val)
    db1.commit()
    print("Member Added Successfully π...")

def showmembers():
    c1 = db1.cursor()
    c1.execute("select * from member")
    res = c1.fetchall()
    #print(res)
    print("List of Members π")
    for val in res:
        print("\t   Name = "+val[1] + "       Aadhar Card= " + val[0])

def addvaccination():
    ad = input("Enter Aadhar Card No. π ")
    name = input("Enter Vaccination Name π ")
    d = input("Enter 1 for Dose 1 , 2 for Dose 2 π ")
    dt = input("Enter the date of Vaccination π ")
    c2 = db1.cursor()
    if d == "1":
        q = "insert into vaccination values(%s,%s,%s,NULL)"
        val = (ad,name,dt)
        c2.execute(q,val)
        db1.commit()
        print("Vaccination Record Added Successfully π...")
    elif d == "2":
        q = "update vaccination set dose2=%s where aadharno=%s"
        val =(dt,ad)
        c2.execute(q,val)
        db1.commit()
        print("Vaccination Record Updated Successfully π...")
    else:
        print("Invalid Input, please try again π«...")
        
def showvaccin():
    c1 = db1.cursor()
    c1.execute("select * from vaccination,member where vaccination.aadharno=member.aadharno")
    res = c1.fetchall()
    #print(res)
    print("List of Vaccinated Members π...")
    print("-"*60)
    print("Name\tVaccine\t   Aadhar No\t Dose1\t         Dose2")
    print("-"*60)
    for val in res:
        print(val[5],val[1],"  ",val[0], "\t",val[2], "\t",val[3])
        
def shownotvaccinated():
    c1 = db1.cursor();
    c1.execute("Select * from member where aadharno not in (select aadharno from vaccination)")
    res = c1.fetchall()
    print("List of Not Vaccinated Members π...")
    print("-"*60)
    print("Name\tAadhar No\tPhone\t  Address\tEmail")
    print("-"*60)
    for val in res:
        print(val[1],  val[0] ,"\t     ",val[3]," ",val[2],"\t",val[4])
        
def showduevaccine():
    c1 = db1.cursor()
    c1.execute("select * from vaccination,member where vaccination.aadharno=member.aadharno and dose2 is null")
    res = c1.fetchall()
    #print(res)
    print("List of Members Whose Dose2 is due π...")
    print("-"*60)
    print("Name     Vaccine   Aadhar No\t Dose1\t        Dose2")
    print("-"*60)
    for val in res:
        print(val[5],val[1]," ",val[0], "\t",val[2], "\t",val[3])
 
def delete_data():
    print("-"*60)

    name = input("Enter Member Name π ")
    cursor1 = db1.cursor()
    q = "delete from member where name='{}'".format(name)
    cursor1.execute(q)
    db1.commit()
    print("Member Deleted Successfully π...")



connect()
print("\t\t Connection Successful...π€")
if login():
    while True:
        print("-" * 60)
        print("\t (πββΏβΏβ)π --- CHOOSE AN OPERATION --- π(ββΏβΏβπ) ")
        print("-" * 60)
        print("Press 1: π Add a New Member")
        print("Press 2: π Add or Update a Vaccination Record")
        print("Press 3: π Show All Members")
        print("Press 4: π Show All Vaccinated Members")
        print("Press 5: π Show Whose Vaccination is Due")
        print("Press 6: π Show Who are not at All Vaccinated")
        print("Press 7: π Delete a Record")
        print("Press 8: π Quit to Exit")
        ch = int(input("Enter Your Choice π "))
        if ch == 1:
            addmember()
        elif ch == 2:
            addvaccination()
        elif ch == 3:
            showmembers()
        elif ch == 4:
            showvaccin()
        elif ch == 5:
            showduevaccine()
        elif ch == 6:
            shownotvaccinated()
        elif ch == 7:
            delete_data()
        elif ch == 8:
            print("\t Thank You ππ§‘\t Byeπ...\t {Programmed by πSHASHWATπ...ππ}")
            break
    
