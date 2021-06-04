# Experimenting with postgis
Set up a table with an eth and pos coolumns

```
CREATE EXTENSION IF NOT EXISTS plpgsql;
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION postgis_raster; -- OPTIONAL
CREATE EXTENSION postgis_topology; -- OPTIONAL

CREATE TABLE ok (
	eth VARCHAR ( 50 ) PRIMARY KEY,
	pos geometry
);
```
Put some fake data into the tables. Those are eth addresses with associated positions.
```
INSERT INTO ok (eth, pos) VALUES ('0x123456789', ST_SetSRID(ST_MakePoint(-71.123456789123456789, 42.3150676015829), 3857));
INSERT INTO ok (eth, pos) VALUES ('0x123456789a', ST_SetSRID(ST_MakePoint(-72, 42.3150676015829), 3857));
INSERT INTO ok (eth, pos) VALUES ('0x123456789b', ST_SetSRID(ST_MakePoint(-4, 8.55), 3857));
```
Run those to check for yourself that the points are stored correctly (WKB: well known binary)
```
SELECT (pos) FROM ok WHERE eth = '0x123456789';
SELECT ST_AsText(ST_PointFromWKB(pos)) FROM ok WHERE eth = '0x123456789';
```
Distance query, this will be slow because we haven't made a spatial index.
```
EXPLAIN SELECT eth, pos <-> ST_SetSRID(ST_MakePoint( 1, 1), 3857) AS dist
FROM ok
ORDER BY dist LIMIT 1;
```
Create the spatial index on the pos column.
```
CREATE INDEX spidx
  ON ok
  USING GIST (pos);
```
Run the same query again and note the speedup (significant even if the db has only a handful of rows)
```
EXPLAIN SELECT eth, pos <-> ST_SetSRID(ST_MakePoint( 1, 1), 3857) AS dist
FROM ok
ORDER BY dist LIMIT 1;
```