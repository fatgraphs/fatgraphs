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


CREATE TABLE IF NOT EXISTS tg_vertex_metadata
(
    id          SERIAL UNIQUE PRIMARY KEY,
    vertex      text,
    type        text,
    label       text,
    description text,
    icon        text
);
CREATE INDEX IF NOT EXISTS eth_index ON tg_vertex_metadata (vertex);

insert into tg_vertex_metadata (vertex, type, label) VALUES ('0x6e71c6d41aed31b18dc37c27dc3309bcdb11e893', 'testing  icons', 'iconic smart contract');

insert into tg_vertex_metadata (vertex, type, label, icon) VALUES ('0x6e71c6d41aed31b18dc37c27dc3309bcdb11e893', 'testing  icons', 'iconic smart contract', 'testicon-ca.png');

insert into tg_vertex_metadata (vertex, type, label, icon) VALUES ('0x9947ea09a045ed3fc427df736463d1b588c06476', 'testing  icons', 'iconic', 'testicon-eoa.png');

insert into tg_vertex_metadata (vertex, type, label) VALUES ('0xe9c1a41b0ba27e80b138c0e17e7cc681b26099cf', 'a guy I know', 'okok');
insert into tg_vertex_metadata (vertex, type, label) VALUES ('0x5719e1bc888efa00dc5b2d992ca364889129a869', 'a guy I know', 'okok');


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

CREATE TABLE IF NOT EXISTS tg_edge
(
    graph_id        int not null,
    src             text,
    trg             text,
    block_number    int,
    amount          real,
    CONSTRAINT fk_graph_id
        FOREIGN KEY (graph_id)
            REFERENCES tg_graphs (id),

    PRIMARY KEY(src, trg, graph_id),

    CONSTRAINT fk_src
        FOREIGN KEY (graph_id, src)
            REFERENCES tg_vertex (graph_id, vertex),

    CONSTRAINT fk_trg
        FOREIGN KEY (graph_id, trg)
            REFERENCES tg_vertex (graph_id, vertex)
) PARTITION BY LIST (graph_id);

