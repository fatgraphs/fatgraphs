-- TODO: if we seed this way we'll have duplication when defining the interface for the corresponding entity
CREATE TABLE IF NOT EXISTS tg_user
(
    name                     text PRIMARY KEY,
    recent_metadata_searches text[]
);

INSERT INTO tg_user
VALUES ('default_user', '{}')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS tg_graphs
(
    id                             SERIAL UNIQUE PRIMARY KEY,
    owner                          text,
    graph_name                     text,
    output_folder                  text,
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
    labels                         text,
    median_pixel_distance          real,
    min                            real,
    max                            real,
    vertices                       bigint,
    edges                          bigint,
    CONSTRAINT fk_owner
        FOREIGN KEY (owner)
            REFERENCES tg_user (name)
);


CREATE TABLE IF NOT EXISTS tg_metadata
(

    id         SERIAL UNIQUE PRIMARY KEY,
    eth_source text,
    eth_target text,
    meta_type  text, -- e.g. label, type
    meta_value text, -- e.g. idex, unused, phising
    entity     text  -- the entity the metadata refers to: e.g. vertex, edge, group of vertices
);

CREATE INDEX IF NOT EXISTS dex_eth_source ON tg_metadata (eth_source);
CREATE INDEX IF NOT EXISTS dex_eth_target ON tg_metadata (eth_target);