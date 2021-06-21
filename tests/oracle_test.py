import cx_Oracle

connection = cx_Oracle.connect(
    user="quizapp",
    password="quizapp1234",
    dsn="localhost:1521")

print("Successfully connected to Oracle Database")

# Obtain a cursor
cursor = connection.cursor()


# Execute the query
sql = "SELECT * FROM questions"
cursor.execute(sql)

# Loop over the result set
for row in cursor:
    print(row)

connection.commit()