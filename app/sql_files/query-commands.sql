SELECT id, title, content, published,
    created_at, owner_id
    FROM course_jwt.posts
LIMIT 1000;

SELECT id, email, password, created_at
    FROM course_jwt.users
LIMIT 1000;

SELECT user_id, post_id
    FROM course_jwt.votes
LIMIT 1000;