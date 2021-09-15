BEGIN;
    CREATE TABLE IF NOT EXISTS tg_account_type(
        vertex text,
        type smallint
    );

    COPY tg_account_type(vertex, type) FROM :v1 WITH (format csv, header);

    COPY tg_account_type(vertex, type) FROM :v2 WITH (format csv, header);

    ALTER TABLE tg_account_type ADD CONSTRAINT vertex_pk PRIMARY KEY (vertex);

COMMIT;