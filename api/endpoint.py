from flask import Flask
from flask import request
from flask import render_template
from prometheus_flask_exporter import PrometheusMetrics
import sql_statements as sql_statements
import json
import requests
import logging


app = Flask(__name__)
metrics = PrometheusMetrics(app)

# static information as metric
metrics.info('app_info', 'Application info', version='1.0.3')

@app.route('/latest')
def latest():
    return str(sql_statements.get_lastest_hanesst_id())
    
@app.route('/post', methods=['POST'])
def post():
    json_string = request.get_json()
    post_type = json_string['post_type']
    print(json_string)
    answere = ""
    
    if(post_type == "story"):
        create_post(json_string)
    elif(post_type == "comment"):
        comment(json_string)
    elif(post_type == "poll"):
        poll()
    elif(post_type == "pollopt"):
        pollopt()
    return answere

@app.route('/project_status')
def project_status():
    status_list = []
    system_message = ""
    status_list.append(get_status_for_ip())
    status_list.append(get_connection_to_db())
    for status in status_list:
        if status == "200":
            system_message = "All Systems Operational"
        else:
            system_message = "A system is down, check below for more info"
    return render_template('status.html', status_list=status_list, system_message=system_message)

def get_status_for_ip():
    ip = 'http://159.65.116.24/home'
    status_code = None
    try:
        status_code = requests.get(ip, timeout=30).status_code
        return status_code
    except requests.ConnectionError as e:
        logging.warning(e)
        return status_code

def get_connection_to_db():
    status_code = None
    try:
        con = sql_statements.make_engine()
        con.close()
        status_code = "200"
        return status_code
    except Exception as e:
        logging.warning(e)
        status_code = "400"
        return status_code
    
@app.route('/status')
def status():
    return "Alive"

def create_post(json_string):
    username = json_string['username']
    password = json_string['pwd_hash']
    user_id = sql_statements.login(username,password)
    if user_id:
        post_title = json_string['post_title']
        hanesst_id = json_string['hanesst_id']
        post_content = json_string['post_url']
        if post_content == None:
            is_url = False
            post_content = json_string['post_text']
        else:   
            is_url = True
        logging.info("Test info")
        logging.debug("Test Debuf")
        logging.info("Request for creating post: title: %s content: %s url: %s user: %s hanesst: %s",post_title,post_content,is_url,user_id,hanesst_id)
        try:
            sql_statements.insert_story(post_title,post_content,is_url,user_id,hanesst_id)
        except Exception as e:
            logging.warning(e)
        
        
    elif user_id == None:
        print("Wrong login")
        try:
            sql_statements.insert_story(post_title,post_content,is_url,543903,hanesst_id)
        except Exception as e:
            logging.warning(e)
        return "Wrong login"

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
    jobject = sql_statements.all_posts()
    post_list = json.loads(jobject)
    return str(post_list)
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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return sort_posts()

@app.route('/create', methods=['GET', 'POST'])
def create():
    username = request.form['acct']
    password = request.form['pw']
    if request.method == 'POST':
        username_taken = sql_statements.check_if_username_is_taken(username)
        if not username_taken:
            sql_statements.insert_user(username, password)
            return render_template('frontpage.html', username=username)
        else:
            return render_template('login.html')
    elif request.method == 'GET':
        sql_statements.login(username, password)
        return render_template('frontpage.html', username=username)
    return

@app.route('/comments')
def comments():
    post_id = request.args.get('post_id')
    sql_dict = sql_statements.comments_from_post(post_id)
    return json.dumps(sql_dict)

@app.route('/comment')
def comment(json_string):
    username = json_string['username']
    password = json_string['pwd_hash']
    user_id = sql_statements.login(username,password)
    if user_id:
        content = json_string['post_text']
        post_parent = json_string['post_parent']
        hanesst_id = json_string['hanesst_id']
        post_id = sql_statements.find_post_with_hanesst_id(post_parent)
        if not post_id:
            comment_dict = sql_statements.find_comment_with_hanesst_id(post_parent)
            post_id = comment_dict['post_id']
            parent_id = comment_dict['id']
            logging.info("Comment on another comment: postid: %s content: %s parentid: %s userid: %s hanesstid: %s",post_id, content, parent_id, user_id, hanesst_id)
            try:
                sql_statements.insert_comment_on_comment(post_id, content, parent_id, user_id, hanesst_id)
            except Exception as e:
                logging.warning(e)
            
        elif post_id:
            logging.info("comment on post: postid: %s content: %s userid: %s hanesstid: %s",post_id, content, user_id, hanesst_id)
            try:
                sql_statements.insert_comment_on_post(post_id, content, user_id, hanesst_id)
            except Exception as e:
                logging.warning(e)
        return

@app.route('/home', methods=['GET', 'POST'])
def sort_posts():
    try:
        if request.method == 'POST':
            post_offset = request.form['post_offset']
        else:
            post_offset = 0
    except Exception as e:
        post_offset = 0
        pass
    jobject = sql_statements.all_posts(post_offset)
    post_list = json.loads(jobject)
    print(post_offset)
    return render_template('frontpage.html', post_list=post_list, post_offset=post_offset)

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',filename='logfile.log',level=logging.DEBUG)
    app.run(host="0.0.0.0", port=5001, debug=True)