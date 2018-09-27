from flask import Flask
from flask import request
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
    sql_statement = f"""
    WITH RECURSIVE cte (id, content, username, path, parent_id, depth, karma)  AS (
    SELECT  
        comments.id,
        content,
        users.username,
        array[-(karma.upvotes - karma.downvotes),comments.id] AS path,
        parent_id,
        1 AS depth,
        karma.upvotes
    FROM 
        ( 
            comments INNER JOIN karma
            ON comments.karma_id = karma.id
            INNER JOIN users
            ON comments.user_id = users.id
        )
    WHERE parent_id IS NULL
        and post_id =  {post_id}
    UNION ALL
    SELECT
        comments.id,
        comments.content,
        users.username,
        cte.path || -(karma.upvotes - karma.downvotes) || comments.id,
        comments.parent_id,
        cte.depth + 1 AS depth,
        karma.upvotes
    FROM    
        ( 
            comments INNER JOIN karma
            ON comments.karma_id = karma.id
            INNER JOIN users
            ON comments.user_id = users.id
        )
    JOIN cte ON comments.parent_id = cte.id
    )
    SELECT 
        id, 
        content,
        username,
        path,
        depth,
        karma
    FROM cte
    ORDER BY path;
    """
    con = db_connect(engine) 
    sqlalchemy_object = con.execute(sql_statement)
    json_list = sqlalchemy_json(sqlalchemy_object)
    con.close()
    return json_list

def sqlalchemy_json(dictionary):
	return json.dumps([dict(r) for r in dictionary],default=str)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")