CREATE OR REPLACE FUNCTION create_tokengallerist(pass varchar) RETURNS void AS $$
        BEGIN
            IF NOT EXISTS (
                SELECT FROM pg_catalog.pg_roles
                WHERE rolname = 'tokengallerist') THEN
				EXECUTE format(
					'CREATE ROLE tokengallerist LOGIN PASSWORD %L'
					 , pass);

                GRANT pg_read_server_files TO tokengallerist; -- needed to load csv files
            END IF;
        END;
$$ LANGUAGE plpgsql;

SELECT create_tokengallerist(:v1);

