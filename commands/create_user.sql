DO
$$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles  -- SELECT list can be empty for this
      WHERE  rolname = 'tokengallerist') THEN

      CREATE ROLE tokengallerist LOGIN PASSWORD '1234';
   END IF;
END
$$;


