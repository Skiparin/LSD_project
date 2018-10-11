from flask import Flask
from flask import request
from flask import render_template
import sql_statements as ss
import json


app = Flask(__name__)
    
@app.route('/post')
def post():
    post = requst.form.get('post_type')
    answere = ""
    if(post == "story"):
        story(request)
    elif(post == "comment"):
        comment()
    elif(post == "poll"):
        poll()
    elif(post == "pollopt"):
        pollopt()
    return answere

def story(request):
    json = request.get_json()
    username = json['username']
    password = json['pwd_hash']
    post_title = json['post_title']
    url = json['post_url']
    sql_statement = ss.login(username,password)
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
    return ss.all_posts()
"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = "orvur"
        password = "1234"
        sql_statement = f"select 1 from users where username = '{username}' and password = '{password}'"
        con = db_connect(engine) 
        sqlalchemy_object = con.execute(sql_statement)
        json_list = sqlalchemy_json(sqlalchemy_object)
        con.close()
    else:
        return render_template('login.html')
    return json_list
"""

@app.route('/create', methods=['POST'])
def create():
    username = request.form.get('acct')
    password = request.form.get('pw')
    username_taken = ss.check_if_username_is_taken(username)
    if not username_taken:
        ss.insert_user(username, password)
        return render_template('frontpage.html', username=username)
    else:
        return render_template('login.html')
    return

@app.route('/comments')
def comments():
    post_id = request.args.get('post_id')
    sql_dict = ss.comments_from_post(post_id)
    return json.dumps(sql_dict)

@app.route('/comment')
def comment():
    #a = request.get.body()
    #comment = a.get('comment')
    #post_id = a.get('post_id')
    #parrent_id = a.get('parrent_id')
    #user_id = a.get('user_id')
    # sql_statement = ss.commment_on_post(comment,post_id,parrent_id,user_id)

    "CONNECTION AND EXCEUTION OF SQL SHOULD BE DONE IN SQL_STATEMENTS"
    #con = db_connect(engine) 
    #sqlalchemy_object = con.execute(sql_statement)
    #con.close()
    return 201

def sqlalchemy_json(dictionary):
	return json.dumps([dict(r) for r in dictionary],default=str)

@app.route('/sortedposts')
def sort_posts():
    jobject = posts()
    post_list = sqlalchemy_json(jobject)
    return render_template('frontpage.html', post_list=post_list)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=5004)
