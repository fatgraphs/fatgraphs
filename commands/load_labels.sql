COPY tg_vertex_metadata(type, eth, label)
FROM :v1
DELIMITER ','
CSV HEADER;