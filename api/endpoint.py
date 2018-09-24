from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from flask.ext.hashing import Hashing
import json


app = Flask(__name__)
hashing = Hashing(app)

DATABASE_CONNECTION = {
    'drivername': 'postgres',
    'port': '5432',
    'username': 'prod',
    'database': 'prod',
}
"""
Makes an engine to the database
"""
engine = create_engine(URL(**DATABASE_CONNECTION))

def db_connect(engine):
    """
    Makes connections to the database
    """
    return engine.connect()

@app.route('/posts')
def posts():
	sql_statement = "Select * from posts"
	con = db_connect(engine)
	sqlalchemy_object = con.execute(sql_statement)
	json_list = sqlalchemy_json(sqlalchemy_object)
    con.close()
	return json_list
	"""
	return json.dumps([dict(r) for r in res])
	"""

@app.route('/login')
def login():
    username = "orvor"
    password = "1234"
    sql_statement = f"Select 1 from users where username = '{username}' and passworld = '{password}'"
    con = db_connect(engine) 
    sqlalchemy_object = con.execute(sql_statement)
    json_list = sqlalchemy_json(sqlalchemy_object)
    con.close()
    return json_list

@app.route('/comments')
def comments(post_id):
    sql_statement = f"Select comments from comments where post_id = '{post_id}'"
    con = db_connect(engine) 
    sqlalchemy_object = con.execute(sql_statement)
    json_list = sqlalchemy_json(sqlalchemy_object)
    con.close()
    return json_list

def sqlalchemy_json(dictionary):
	return json.dumps([dict(r) for r in dictionary],default=str)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
