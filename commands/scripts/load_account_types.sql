BEGIN;
    CREATE TABLE IF NOT EXISTS tg_account_type(
        vertex text,
        type smallint
    );

    COPY tg_account_type(vertex, type) FROM :v1 WITH (format csv, header);

    COPY tg_account_type(vertex, type) FROM :v2 WITH (format csv, header);

    ALTER TABLE tg_account_type ADD CONSTRAINT vertex_pk PRIMARY KEY (vertex);

COMMIT;

insert into tg_account_type (vertex, type) VALUES ('0xe9c1a41b0ba27e80b138c0e17e7cc681b26099cf', 1);
insert into tg_account_type (vertex, type) VALUES ('0xef51c9377feb29856e61625caf9390bd0b67ea18', 1);
insert into tg_account_type (vertex, type) VALUES ('0x997c48ce1af0ce2658d3e4c0bea30a0eb9c98382', 1);