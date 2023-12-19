DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'kiavash') THEN
      
      CREATE ROLE kiavash LOGIN PASSWORD 'password';
   END IF;
END
$do$;

DO
$do$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'focusedai') THEN
      PERFORM dblink_exec('dbname=' || current_database()
                        , 'CREATE DATABASE focusedai');
   END IF;
END
$do$;
GRANT ALL PRIVILEGES ON DATABASE focusedai TO kiavash;
