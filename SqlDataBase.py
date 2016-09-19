'''
The module that handles the
data base management of the
spelling helper

is a subset of the Textwork.py
module
'''
import sqlite3, time

def add_name(name, speed=1.5):
    '''add a name to the dataBase'''
    global c, conn

    assert isinstance(name, str), "Incorrect type input"
    try:
        c.execute("INSERT INTO nameDataBase (word) VALUES (?)", (name,))
        conn.commit()
        print("Processing...");time.sleep(speed);print("Finished\n")
    except Exception as e:
        print("Error adding name to database at SqlModule: \n"+str(e))

def add_defintion(name, defintion):
    '''add a defintion and a name
    to the data base'''
    global c, conn

    try:
        c.execute("INSERT INTO definitionDataBase (name, definition) VALUES (?, ?)", (name, defintion))
        conn.commit()
        print("Processing...");time.sleep(1.5);print("Finished\n")
    except Exception as e:
        print("Error adding a definition at SqlModule: \n"+str(e))

def display_database(*database):
    '''sends a list to the reqister of all the values in the database'''
    global c

    to_display = list(database)
    if len(to_display) > 1:
        c.execute("SELECT * FROM nameDataBase");data = c.fetchall()
        c.execute("SELECT * FROM definitionDataBase");dictionary = c.fetchall()
        names, defin = [], []
        for row in data:
            names.append(row[0])
        for row in dictionary:
            defin.append(row[0])
        return names, defin
    else:
        to_execute = "SELECT * FROM {}DataBase".format(database[0])
        c.execute(to_execute);data = c.fetchall()
        return_list = []
        for row in data:
            if len(return_list) < 40:
                return_list.append(row[0])
        return return_list

def find_definition(word):
    '''Finds a definition or word from the database'''
    global c

    try:
        exec_str = "SELECT definition FROM definitionDataBase WHERE name = '{}'".format(word)
        c.execute(exec_str);data = c.fetchall()
        return data[0][0]
    except Exception as e:
        print("Failed:"+str(e))
        return False

def list_similar(character):
    '''Returns all the words that are similar to word'''
    global c

    exec_str = "SELECT * from nameDataBase WHERE word LIKE '{}'".format(character+"%")
    c.execute(exec_str);data = c.fetchall()
    priority = [];included = []
    for row in data:
        if len(priority + included) <= 40:
            if row[0][0] == character[0]:
                if character in row[0]:
                    priority.append(row[0])
                else:
                    included.append(row[0])
        else:
            break
    return priority + included

def create_dataBase():
    global c
    c.execute("CREATE TABLE IF NOT EXISTS nameDataBase(word TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS definitionDataBase(name Text, definition Text)")

def close():
    '''Closes the sql database'''
    global c, conn

    if conn:
        c.close()
    print("Sql DataBase Closed")

def prepare_main():
    '''run the setup for the data bases'''
    global c, conn

    conn = sqlite3.connect('definition.db')
    c = conn.cursor()

    #create_dataBase()

def fast_add(name):
    '''add a name to the dataBase'''
    global c, conn
    c.execute("INSERT INTO nameDataBase (word) VALUES (?)", (name,))
    conn.commit()
    time.sleep(0.5)

#Load MIT Word list into DataBase
def load():
    try:
        with open("wordlist.txt", 'r') as wordList:
            for item in wordList:
                print("Adding", item[:-1])
                fast_add(item[:-1])
        if wordList.closed:
            print("Good to go!")
    except Exception as e:
        print(str(e))

def test_find(word):
    '''To test for faster ways to access the database
    word is the live character string'''
    global c

    st = "SELECT * FROM nameDataBase WHERE word LIKE '{}'".format(word+"%")
    c.execute(st);data = c.fetchall()
    print(data)


if __name__ == '__main__':prepare_main()
