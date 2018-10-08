from flask import Flask
from flask import request
from flask import render_template
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
import sql_statements as ss
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
@app.route(/'post')
def post():
    post = requst.form.get('post_type')
    answere = ""
    if(post = "story"):
        story(request)
    elif(post = "comment"):
        comment()
    elif(post = "poll"):
        poll()
    elif(post = "pollopt"):
        pollopt()
    return answere

def story(request):
    json = request.get_json()
    username = json['username']
    password = json['pwd_hash']
    post_title = json['post_title']
    url = json['post_url']
    sql_statement = ss.login(username,password)
    con = db_connect(engine)
    sqlalchemy_object = con.execute(sql_statement)
    json_list = sqlalchemy_json(sqlalchemy_object)
    con.close()
    return "story"

    #Post on frontpage
def comment():
    return "comment"
    #Post a comment
def poll():
    return "poll"
    #Poll, just throw away
def pollopt():
    return "pollopt"
    #Poll options, just throw away
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
    sql_statement = ss.comments_from_post(post_id)
    con = db_connect(engine) 
    sqlalchemy_object = con.execute(sql_statement)
    json_list = sqlalchemy_json(sqlalchemy_object)
    con.close()
    return json_list

@app.route('/comment')
def comment():
    #a = request.get.body()
    #comment = a.get('comment')
    #post_id = a.get('post_id')
    #parrent_id = a.get('parrent_id')
    #user_id = a.get('user_id')
    # sql_statement = ss.commment_on_post(comment,post_id,parrent_id,user_id)
    con = db_connect(engine) 
    sqlalchemy_object = con.execute(sql_statement)
    con.close()
    return 201

def sqlalchemy_json(dictionary):
	return json.dumps([dict(r) for r in dictionary],default=str)

@app.route('/sortedposts')
def sort_posts():
    jobject = posts()
    post_list = json.loads(jobject)
    return render_template('frontpage.html', post_list=post_list)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=5001)
