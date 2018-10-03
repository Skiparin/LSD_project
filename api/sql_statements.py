def comments_from_post(post_id):
    return f"""
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