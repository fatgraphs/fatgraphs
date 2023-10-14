BEGIN;
    CREATE TABLE IF NOT EXISTS tg_vertex_metadata
    (
        id          SERIAL UNIQUE PRIMARY KEY,
        graph_id    int,
        vertex      text not null,
        type        text,
        account_type    int,
        label       text,
        description text,
        icon        text,
        CONSTRAINT fk_vertex
            FOREIGN KEY (graph_id, vertex)
                REFERENCES tg_vertex (graph_id, vertex)
    );

    COPY tg_vertex_metadata(graph_id,vertex,type,account_type,label,description,icon) FROM :v1 WITH (format csv, header);

    CREATE INDEX IF NOT EXISTS eth_index ON tg_vertex_metadata (vertex);
    CREATE INDEX IF NOT EXISTS account_type_index ON tg_vertex_metadata (account_type);
    CREATE INDEX IF NOT EXISTS label_index ON tg_vertex_metadata (label);
COMMIT;



