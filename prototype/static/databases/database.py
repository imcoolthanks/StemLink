import mysql.connector
database=mysql.connector.connect(user="root" , password="25121984",host="127.0.0.1", database="ypsteml")

def create_student(data):#creates a new student from the given data given to it
    cnx=database.cursor()
    cnx.execute(f"INSERT INTO students (ID,name,password,email,imageUrl,age,country,State,Interests,mentors) VALUES ({data[0]}, '{data[1]}', '{data[2]}', '{data[3]}','{data[4]}','{data[5]}','{data[6]}','{data[7]}','{data[8]}','{data[9]}');")
    cnx.execute(f"INSERT INTO ids(ID) VALUES({data[0]});")
    database.commit()

    
def create_mentor(data):#creates a new mentor
    cnx=database.cursor()
    cnx.execute(f"INSERT INTO mentor (ID,name,password,email,ImageUrl,Age,Country,State,Interests,Students) VALUES ({data[0]},'{data[1]}','{data[2]}', '{data[3]}','{data[4]}','{data[5]}','{data[6]}','{data[7]}','{data[8]}','{data[9]}');")
    cnx.execute(f"INSERT INTO ids(ID) VALUES('{data[0]}');")
    database.commit()
def get_number_of_ids():
    cnx=database.cursor()
    cnx.execute("select count(*) from ids")  
    return list(cnx)
def get_mentors():
    cnx=database.cursor()
    cnx.execute("select * from mentor;")
   
    return cnx



