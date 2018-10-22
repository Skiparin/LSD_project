from flask import Flask
from flask import request
from flask import render_template
import sql_statements as ss
import json


app = Flask(__name__)
    
@app.route('/post', methods=['POST'])
def post():
    json = request.get_json()
    post_type = json['post_type']
    print(post_type)
    answere = ""
    if(post_type == "story"):
        story(json)
    elif(post_type == "comment"):
        comment()
    elif(post_type == "poll"):
        poll()
    elif(post_type == "pollopt"):
        pollopt()
    return answere

def create_post(json):
    username = json['username']
    password = json['pwd_hash']
    print(username)
    print(password)
    user_id = ss.login(username,password)
    print(user_id)
    if user_id != None:
        post_title = json['post_title']
        hanesst_id = json['hanesst_id']
        post_content = json['post_url']
        if post_content == None:
            is_url = False
            post_content = json['post_text']
        else:   
            is_url = True
        ss.insert_story(post_title,post_content,is_url,user_id,hanesst_id)
    elif user_id == None:
        print("Wrong login")
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
    return ss.all_posts()

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
    username = json['username']
    password = json['psw_hash']
    user_id = ss.login(username,password)
    if user_id != None:
        content = json['post_text']
        post_parent = json['post_parent']
        hanesst_id = json['hanesst_id']
        post_id = ss.find_post_with_hanesst_id(post_parent)
        if post_id == None:
            comment_dict = find_comment_with_hanesst_id(parent_id)
            post_id = comment_dict['post_id']
            parent_id = comment_dict['id']
            insert_comment_on_comment(post_id, content, parent_id, user_id, hanesst_id)
        elif post_id != None:
            insert_comment_on_post(post_id, content, user_id, hanesst_id)
        return





def sqlalchemy_json(dictionary):
	return json.dumps([dict(r) for r in dictionary],default=str)

@app.route('/sortedposts')
def sort_posts():
    jobject = ss.all_posts()
    post_list = json.loads(jobject)
    return render_template('frontpage.html', post_list=post_list)


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=5002)
