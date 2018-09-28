from flask import Flask
from flask import request
from flask import render_template
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
    sql_statement = "select * from posts"
    con = db_connect(engine)
    sqlalchemy_object = con.execute(sql_statement)
    json_list = sqlalchemy_json(sqlalchemy_object)
    con.close()
    return json_list

@app.route('/login')
def login():
    username = "orvor"
    password = "1234"
    sql_statement = f"select 1 from users where username = '{username}' and passworld = '{password}'"
    con = db_connect(engine) 
    sqlalchemy_object = con.execute(sql_statement)
    json_list = sqlalchemy_json(sqlalchemy_object)
    con.close()
    return json_list

@app.route('/comments')
def comments():
    post_id = request.args.get('post_id')
    sql_statement = f"select * from comments where post_id = '{post_id}'"
    con = db_connect(engine) 
    sqlalchemy_object = con.execute(sql_statement)
    json_list = sqlalchemy_json(sqlalchemy_object)
    con.close()
    return json_list

def sqlalchemy_json(dictionary):
	return json.dumps([dict(r) for r in dictionary],default=str)



@app.route('/sortedposts')
def sort_posts():
    jobject = posts()
    post_list = json.loads(jobject)
    return str(post_list)
    #return render_template('frontpage.html', post_list=post_list)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=5001)
