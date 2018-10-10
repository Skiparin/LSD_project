from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

DATABASE_CONNECTION = {
    'drivername': 'postgres',
    'port': '5432',
    'username': 'prod',
    'database': 'prod',
}
"""
Makes an engine to the database
"""
def create_engine():
    engine = create_engine(URL(**DATABASE_CONNECTION))
    return engine

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
    engine = create_engine()
    con = db_connect(engine)
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
        username = {username} 
        and 
        password = {password}
    """
    engine = create_engine()
    con = db_connect(engine)
    sqlalchemy_object = con.execute(sql_statement)
    user_id = sqlalchemy_object.fetchone()[0]
    con.close()
    return user_id

def check_if_username_is_taken(username):
    sql_statement = f"""
    select
        1 
    from 
        users 
    where 
        username = '{username}'
    """
    engine = create_engine()
    con = db_connect(engine)
    sqlalchemy_object = con.execute(sql_statement)
    value = sqlalchemy_object.fetchone()[0]
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
        {username},
        {password}
        )
    """
    engine = create_engine()
    con = db_connect(engine)
    con.execute(sql_statement)
    con.close()

def all_posts():
    sql_statement = f"""
    select
        *
    from
        posts
    """
    engine = create_engine()
    con = db_connect(engine)
    sqlalchemy_object = con.execute(sql_statement)
    posts = sqlalchemy_object.fetchone()[0]
    con.close()
    return posts

