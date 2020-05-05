/*this file takes the hh_2o_4pgr table that was constructed by osm2po
and creates a table extracting the unique nodes*/
SELECT source AS node, 
st_startpoint(geom_way) AS geom
INTO ungrouped_nodes
FROM hh_2po_4pgr;

INSERT INTO ungrouped_nodes
SELECT target AS node, 
st_endpoint(geom_way) AS geom
FROM hh_2po_4pgr;

SELECT * 
INTO road_nodes
FROM ungrouped_nodes
GROUP BY 1,2;

DROP TABLE ungrouped_nodes;