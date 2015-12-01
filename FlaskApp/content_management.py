import MySQLdb

def Content():
    TOPIC_DICT = {"Basics":[["Introduction to Python","/introduction-to-python-programming/"],
                            ["Print functions and Strings","/python-tutorial-print-function-strings/"],
                            ["Math basics with Python 3","/math-basics-python-3-beginner-tutorial/"]],
                  "Web Dev":[]}

    return TOPIC_DICT

def connect_to_db():
	conn = MySQLdb.connect(host="localhost", 
							user="root",
							passwd="root",
							db="pythonprogramming")
	c = conn.cursor()
	return c, conn
