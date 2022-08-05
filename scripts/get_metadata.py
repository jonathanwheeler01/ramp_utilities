import pandas as pd
import sqlite3

# Create a connection to a database
con = sqlite3.connect('./metadata_database/rampdata.db')

# intialize a cursor to interact with the database
cur = con.cursor()

# run a query
res = cur.execute('SELECT ir FROM repositories')

# see the result
print(res.fetchone())

