CREATE TABLE IF NOT EXISTS gallery_categories
(
    id          SERIAL UNIQUE PRIMARY KEY,
    title       text UNIQUE,
    description CHAR(155),
    freetext    text,
    urlslug     text UNIQUE
);

CREATE TABLE IF NOT EXISTS tg_graphs
(
    id                             SERIAL UNIQUE PRIMARY KEY,
    graph_name                     text,
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
    vertices                       bigint,
    edges                          bigint,
    graph_category                 int,
    CONSTRAINT fk_graph_category
        FOREIGN KEY (graph_category)
            REFERENCES gallery_categories (id)
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


CREATE TABLE IF NOT EXISTS tg_vertex
(
    graph_id    int not null,
    vertex      text,
    size        real,
    pos         Geometry('Point', 3857),
    CONSTRAINT fk_graph_id
        FOREIGN KEY (graph_id)
            REFERENCES tg_graphs (id)
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
            REFERENCES tg_graphs (id)
) PARTITION BY LIST (graph_id);


INSERT INTO gallery_categories VALUES (1, 'default',  'The default category', '', 'default');
INSERT INTO gallery_categories VALUES (2, 'token_networks',  'Token networks graphs', '', 'token');
INSERT INTO gallery_categories VALUES (3, 'dex',  'Decentralised exchanges', '', 'dex');
INSERT INTO gallery_categories VALUES (4, 'defiapps',  'Decentralised finance applications', '', 'defi');



