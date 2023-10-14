CREATE TABLE IF NOT EXISTS gallery_categories
(
    id          SERIAL UNIQUE PRIMARY KEY,
    title       text UNIQUE,
    description CHAR(155),
    freetext    text,
    urlslug     text UNIQUE
);
INSERT INTO gallery_categories VALUES (1, 'default',  'The default category', '', 'default');
INSERT INTO gallery_categories VALUES (2, 'token_networks',  'Token networks graphs', '', 'token');
INSERT INTO gallery_categories VALUES (3, 'dex',  'Decentralised exchanges', '', 'dex');
INSERT INTO gallery_categories VALUES (4, 'defiapps',  'Decentralised finance applications', '', 'defi');

CREATE TABLE IF NOT EXISTS tg_graphs
(
    id                             SERIAL UNIQUE PRIMARY KEY,
    graph_name                     text,
    description                    text,
    graph_category                 int,
    vertices                       bigint,
    edges                          bigint,
    CONSTRAINT fk_graph_category
        FOREIGN KEY (graph_category)
            REFERENCES gallery_categories (id)
);

CREATE TABLE IF NOT EXISTS tg_graph_configs
(
    id                             SERIAL UNIQUE PRIMARY KEY,
    tile_size                      bigint,
    zoom_levels                    bigint,
    min_transparency               double precision,
    max_transparency               double precision,
    tile_based_mean_transparency   double precision,
    std_transparency_as_percentage double precision,
    max_edge_thickness             double precision,
    med_edge_thickness             double precision,
    max_vertex_size                double precision,
    med_vertex_size                double precision,
    curvature                      double precision,
    bg_color                       text,
    source                         text,
    median_pixel_distance          real,
    min                            real,
    max                            real,
    graph                 int,
    CONSTRAINT fk_graph
        FOREIGN KEY (graph)
            REFERENCES tg_graphs (id)
);



CREATE TABLE IF NOT EXISTS tg_vertex
(
    graph_id    int not null,
    vertex      text,
    size        real,
    pos         Geometry('Point', 3857),
    CONSTRAINT fk_graph_id
        FOREIGN KEY (graph_id)
            REFERENCES tg_graphs (id),

    PRIMARY KEY(graph_id, vertex)

) PARTITION BY LIST (graph_id);



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
CREATE INDEX IF NOT EXISTS eth_index ON tg_vertex_metadata (vertex);

insert into tg_vertex_metadata (vertex, type, label) VALUES ('0xd48ae76be7ff70be6fc2d7a3fa07734f7b73d7af', 'testing  icons', 'iconic smart contract');

insert into tg_vertex_metadata (vertex, type, label, icon) VALUES ('0x6e71c6d41aed31b18dc37c27dc3309bcdb11e893', 'testing  icons', 'iconic smart contract', 'testicon-ca.png');

insert into tg_vertex_metadata (vertex, type, label, icon) VALUES ('0x9947ea09a045ed3fc427df736463d1b588c06476', 'testing  icons', 'iconic', 'testicon-eoa.png');

insert into tg_vertex_metadata (vertex, type, label, account_type) VALUES 
    ('0xe9c1a41b0ba27e80b138c0e17e7cc681b26099cf', 'test_type', 'some_label', 1);
insert into tg_vertex_metadata (vertex, type, label) VALUES ('0x5719e1bc888efa00dc5b2d992ca364889129a869', 'test_type', 'some_label');
insert into tg_vertex_metadata (vertex, type, label) VALUES ('0xe9ff7df19b57f182efacaa3eab73a4bdccff46df', 'test_type', 'not_that_label');

insert into tg_vertex_metadata (vertex, account_type) VALUES ('0x62243a732a77b0c6483ae7ed1b6377da0668b205', 1);
insert into tg_vertex_metadata (vertex, account_type, label) VALUES ('0x0ea9b6713849d92ce71bd4beeedc08bdaf3d51d1', 1, 'one_label');
insert into tg_vertex_metadata (vertex, account_type) VALUES ('0x4cd846d65092f2b80ce07e799db4def99dd43e74', 0);
insert into tg_vertex_metadata (vertex, account_type, label) VALUES ('0x8533a0bd9310eb63e7cc8e1116c18a3d67b1976a', 0, 'more_labelss');


CREATE TABLE IF NOT EXISTS tg_edge
(
    graph_id        int not null,
    src_id          text,
    trg_id          text,
    block_number    int,
    amount          real,
    CONSTRAINT fk_graph_id
        FOREIGN KEY (graph_id)
            REFERENCES tg_graphs (id),

    PRIMARY KEY(src_id, trg_id, graph_id),

    CONSTRAINT fk_src
        FOREIGN KEY (graph_id, src_id)
            REFERENCES tg_vertex (graph_id, vertex),

    CONSTRAINT fk_trg
        FOREIGN KEY (graph_id, trg_id)
            REFERENCES tg_vertex (graph_id, vertex)
) PARTITION BY LIST (graph_id);

