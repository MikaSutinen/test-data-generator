DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM information_schema.schemata WHERE schema_name = 'test') THEN
    CREATE SCHEMA test;
    RAISE NOTICE 'Schema "test" created';
  ELSE
    RAISE NOTICE 'Schema "test" already exists';
  END IF;
END $$;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'test' AND tablename = 'users') THEN
    CREATE TABLE test.users
    (
      id SERIAL PRIMARY KEY,
      name TEXT NOT NULL,
      email TEXT UNIQUE NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    RAISE NOTICE 'Table "users" created';
  ELSE
    RAISE NOTICE 'Table "users" already exists';
  END IF;
END $$;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'test' AND tablename = 'posts') THEN
    CREATE TABLE test.posts
    (
      id SERIAL PRIMARY KEY,
      title TEXT NOT NULL,
      content TEXT NOT NULL,
      user_id INTEGER NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES test.users(id)
    );
    RAISE NOTICE 'Table "posts" created';
  ELSE
    RAISE NOTICE 'Table "posts" already exists';
  END IF;
END $$;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'test' AND tablename = 'comments') THEN
    CREATE TABLE test.comments
    (
      id SERIAL PRIMARY KEY,
      content TEXT NOT NULL,
      post_id INTEGER NOT NULL,
      user_id INTEGER NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (post_id) REFERENCES test.posts(id),
      FOREIGN KEY (user_id) REFERENCES test.users(id)
    );
    RAISE NOTICE 'Table "comments" created';
  ELSE
    RAISE NOTICE 'Table "comments" already exists';
  END IF;
END $$;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM information_schema.views WHERE table_schema = 'test' AND table_name = 'user_post_count') THEN
    CREATE VIEW test.user_post_count AS
    SELECT 
      u.id AS user_id,
      u.name,
      COUNT(p.id) AS post_count
    FROM 
      test.users u
      LEFT JOIN test.posts p ON u.id = p.user_id
    GROUP BY 
      u.id, u.name;
    RAISE NOTICE 'View "user_post_count" created';
  ELSE
    RAISE NOTICE 'View "user_post_count" already exists';
  END IF;
END $$;

DO $$
BEGIN
  CREATE OR REPLACE FUNCTION get_user_posts(p_user_id INT)
  RETURNS TABLE(name TEXT, email TEXT, post_id INT, title TEXT, content TEXT, created_at TIMESTAMP)
  LANGUAGE plpgsql
  AS $$
  BEGIN
      RETURN QUERY
      SELECT usr.name, usr.email, ps.id AS post_id, ps.title, ps.content, ps.created_at
      FROM test.users AS usr
      INNER JOIN test.posts AS ps ON usr.id = ps.user_id
      WHERE usr.id = p_user_id;
  END $$;