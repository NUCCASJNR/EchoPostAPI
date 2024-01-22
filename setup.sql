-- sql script


CREATE DATABASE IF NOT EXISTS blog_db;
       CREATE USER IF NOT EXISTS 'blog_user'@'localhost' IDENTIFIED BY 'blog_pwd';
              GRANT ALL PRIVILEGES ON blog_db.* TO 'blog_user'@'localhost';
                                      GRANT SELECT ON performance_schema.* TO 'blog_user'@'localhost';
FLUSH PRIVILEGES;