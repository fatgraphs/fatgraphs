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
    edges                          bigint
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



