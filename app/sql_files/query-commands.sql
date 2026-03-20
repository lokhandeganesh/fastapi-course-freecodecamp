SELECT id, title, content, published,
    created_at, owner_id
    FROM course.posts
LIMIT 1000;

SELECT id, email, password, created_at
    FROM course.users
LIMIT 1000;

SELECT user_id, post_id
    FROM course.votes
LIMIT 1000;

DELETE FROM course.users
    WHERE id = 'b3c3d0e2-1a4a-409c-b5f4-9bfb04e27e3d'