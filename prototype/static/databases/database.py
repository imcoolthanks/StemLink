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


def check_if_user_exists(email,password):
    cnx=database.cursor()
    print(f"select count(*) from students WHERE name='{email}' and password='{password}';")
    cnx.execute(f"select count(*) from students WHERE name='{email}' and password='{password}';")
    student=list(cnx)[0][0]
    
    cnx.execute(f'select count(*) from mentor WHERE name="{email}" and password="{password}";')
    mentor=list(cnx)[0][0]
    return [student,mentor]
def get_specific_student(email,password):
    cnx=database.cursor()
    cnx.execute(f'select name,Interests,password,email, age,state,id from students where name="{email}" and password="{password}";')
    return list(cnx)
def get_specific_student_id(id):
    cnx=database.cursor()
    cnx.execute(f'select name,Interests,password,email, age,state,id from students where ID={id};')
    return list(cnx)
def update(type,update_name,value,id):
    cnx=database.cursor()
    print(f"UPDATE {type} SET {update_name}={value} WHERE ID={id};")
    cnx.execute(f'UPDATE {type} SET {update_name}="{value}" WHERE ID={id};')
    database.commit()

def get_similar_interests(type,interest):
    cnx=database.cursor()
    print(f'select ID from students where Interests like "%{interest}%";')
    cnx.execute(f'select ID from students where Interests like "%{interest}%";')
    print(cnx)

    return list(cnx)
    