from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
import json
app = Flask(__name__)


DATABASE_CONNECTION = {
    'drivername': 'postgres',
    'port': '5432',
    'username': 'prod',
    'database': 'prod',
}

def db_connect():
    """
    Connect to database where we'll save properties.
    """
    engine = create_engine(URL(**DATABASE_CONNECTION))
    return engine.connect()

@app.route('/posts')
def posts():
	sql_statement = "Select * from posts"
	con = db_connect()
	sqlalchemy_object = con.execute(sql_statement)
	json_list = sqlalchemy_json(sqlalchemy_object)
	return json_list
	"""
	return json.dumps([dict(r) for r in res])
	"""

def sqlalchemy_json(dictionary):
	return json.dumps([dict(r) for r in dictionary],default=str)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
