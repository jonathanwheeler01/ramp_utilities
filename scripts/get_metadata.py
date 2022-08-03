import pandas as pd
import sqlite3

# Create a connection to a database
con = sqlite3.connect('../metadata_database/irmeta.sqlite')

# intialize a cursor to interact with the database
cur = con.cursor()

# run a query
res = cur.execute('SELECT count(*) FROM repositories')

# see the result
print(res.fetchone())

