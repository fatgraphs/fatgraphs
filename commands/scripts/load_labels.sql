COPY tg_vertex_metadata(type, vertex, label)
FROM :v1
DELIMITER ','
CSV HEADER;

