import sqlite3 as sql

def create_users():
    #Create database file/connect to it
    conn = sql.connect("users.db")

    #Create table
    conn.execute("""CREATE TABLE users (email TEXT PRIMARY KEY, password TEXT, name TEXT, age INT, role TEXT, pfp_url TEXT) 
                                            """)

    print("table created")

    conn.close()

def new_user(row): #Pass in an array of info (email, password, name, age, role) like this

    #Connect to database
    conn = sql.connect("users.db")
    cur = conn.cursor()

    #Load all rows
    insert_query = """INSERT INTO users (email, password, name, age, role, pfp_url) 
                                        VALUES (?,?,?,?,?,?)"""
    cur.execute(insert_query, (row[0], row[1], row[2], row[3], row[4], row[5]))

    #Save changes
    conn.commit()

    conn.close()

    print("Loading completed")

#DEBUGGING ---- DELETE
def list_user():
    # if os.path.isfile("prototype/static/databases/bursary_database.db"):
    #     con = sqlite3.connect("prototype/static/databases/bursary_database.db")

    conn = sql.connect("users.db")
    cur = conn.cursor()

    cur.execute("select * from users")
    
    rows = list(cur.fetchall())

    return rows

def create_new():
    create_users()
    new_user(("123@gmail.com","123","Rick",123,"student","default_user_icon.jpg"))
    list_user()

list_user()