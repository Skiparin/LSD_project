from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.sql import text
from sqlalchemy.pool import Pool, NullPool
import json

DATABASE_CONNECTION = {
    'drivername': 'postgres',
    'port': '5432',
    'username': 'prod',
    'database': 'prod',
}
"""
Makes an engine to the database
"""
def make_engine():
    engine = create_engine(URL(**DATABASE_CONNECTION), poolclass=NullPool)
    return engine.connect()

def sqlalchemy_json(dictionary):
    return json.dumps([dict(r) for r in dictionary],default=str)

def comments_from_post(post_id):
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
    con = make_engine()
    sqlalchemy_object = con.execute(sql_statement)
    sql_dict = sqlalchemy_json(sqlalchemy_object)
    con.close()
    return sql_dict

def login(username, password):
    sql_statement = f"""
    select 
        id 
    from 
        users 
    where 
        username = '{username}' 
        and 
        password = '{password}' 
    """
    con = make_engine()
    sqlalchemy_object = con.execute(sql_statement)
    user_id = None
    for sql_tuble in sqlalchemy_object:
        user_id = sql_tuble[0]
    con.close()
    return user_id

def insert_story(post_title, post_content, is_url, user_id, hanesst_id):
    sql_statement = """
    INSERT INTO
        posts(
                title,
                content,
                is_link,
                user_id,
                hanesst_id
            )
        values(
                :post_title, 
                :post_content, 
                :is_url, 
                :user_id, 
                :hanesst_id
            )
    """
    con = make_engine()
    con.execute(text(sql_statement), post_title=post_title, post_content=post_content, is_url=is_url,user_id=user_id,hanesst_id=hanesst_id)
    con.close()

def insert_comment_on_post(post_id,content,user_id,hanesst_id):
    sql_statement = """
    INSERT INTO
        comments(
                post_id,
                content,
                user_id,
                hanesst_id
            )
        values(
                :post_id,
                :content,
                :user_id,
                :hanesst_id
            )
    """
    con = make_engine()
    con.execute(text(sql_statement), post_id=post_id,content=content, user_id=user_id,hanesst_id=hanesst_id)
    con.close()
def insert_comment_on_comment(post_id,content,parent_id,user_id,hanesst_id):
    sql_statement = """
    INSERT INTO
        comments(
                post_id,
                content,
                parent_id,
                user_id,
                hanesst_id
            )
        values(
                :post_id,
                :content,
                :parent_id,
                :user_id,
                :hanesst_id
            )
    """
    con = make_engine()
    con.execute(text(sql_statement), post_id=post_id,content=content, parent_id=parent_id,user_id=user_id,hanesst_id=hanesst_id)
    con.close()
def find_comment_with_hanesst_id(hanesst_id):
    sql_statement = """
        SELECT
            id,
            post_id
        FROM
            comments
        WHERE
            hanesst_id = :hanesst_id
        """
    con = make_engine()
    sqlalchemy_object = con.execute(text(sql_statement),hanesst_id=hanesst_id)
    value = None
    for sql_tuple in sqlalchemy_object:
        value = {}
        for x,y in sql_tuple.items():
            value[x] = y
            print(str(value))
    return value
    con.close()

def find_post_with_hanesst_id(hanesst_id):
    sql_statement = """
        SELECT 
            id
        FROM
            posts
        WHERE 
            hanesst_id = :hanesst_id
        """
    con = make_engine()
    sqlalchemy_object = con.execute(text(sql_statement),hanesst_id=hanesst_id)
    value = None
    for sql_tuple in sqlalchemy_object:
        value = sql_tuple[0]
    con.close()
    return value
    
def check_if_username_is_taken(username):
    sql_statement = f"""
    select
        1
    from 
        users 
    where 
        username = '{username}'
    """
    con = make_engine()
    sqlalchemy_object = con.execute(sql_statement)
    value = None
    for sql_tuple in sqlalchemy_object:
        value = sql_tuple[0]
    con.close()
    return value

def insert_user(username, password):
    sql_statement = f"""
    insert into 
        users
            (
            username,
            password
            )
    values
        (
        :username,
        :password''
        )
    """
    con = make_engine()
    con.execute(text(sql_statement),username=username,password=password)
    con.close()

def get_lastest_hanesst_id():
    sql_statement = f"""
    SELECT
        case 
            when max(p.hanesst_id) > max(c.hanesst_id) 
            THEN max(p.hanesst_id) 
        ELSE max(c.hanesst_id) 
        end 
    from 
        posts p 
        full outer join comments c
        on 
            p.hanesst_id = c.hanesst_id;

    """
    con = make_engine()
    sqlalchemy_object = con.execute(sql_statement)
    value = None
    for sql_tuple in sqlalchemy_object:
        value = sql_tuple[0]
    con.close()
    return value

def all_posts():
    sql_statement = f"""
    select
        *
    from
        posts
    order by
        modified_on
    desc
    limit 30
    """
    con = make_engine()
    sqlalchemy_object = con.execute(sql_statement)
    posts = sqlalchemy_json(sqlalchemy_object)
    con.close()
    return posts