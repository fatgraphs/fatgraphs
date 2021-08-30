COPY tg_vertex_metadata(type, eth, label, icon)
FROM :v1
DELIMITER ','
CSV HEADER;