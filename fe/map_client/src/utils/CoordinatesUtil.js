/**
 * Given a graph coordinate (as generated by force atlas 2) it returns the
 * corresponding coordinate on the map.
 *
 * @param graph_coordinate
 * @param g_min: this should be the smallest number appearing either as x or y among all
 * the coordinates of the graph
 * @param g_max same as g_min but the largest number
 * @param tile_size tile size used when generating the graph tiles
 */
export function convert_graph_coordinate_to_map(graph_coordinate, g_min, g_max, tile_size) {
    // console.log("graph_coordinate" + graph_coordinate)
    // console.log(g_min)
    // console.log(g_max)
    let graph_side = g_max - g_min
    // console.log("graph sixe: " + graph_side)
    let map_x = -1 * (graph_coordinate[1] + Math.abs(g_min)) * tile_size / graph_side
    let map_y = (graph_coordinate[0] + Math.abs(g_min)) * tile_size / graph_side
    // console.log([-map_y, map_x])
    return [map_x, map_y]
}

/**
 * Inverse of convert_graph_coordinate_to_map
 */
export function convert_map_coordinate_to_graph(map_coordinate, g_min, g_max, tile_size){
    let graph_side = g_max - g_min
    console.log("graph sixe: " + graph_side)
    let graph_x = (map_coordinate[1] * graph_side / tile_size) - Math.abs(g_min)
    let graph_y = -(map_coordinate[0] * graph_side / tile_size) - Math.abs(g_min)
    // console.log([-map_y, map_x])
    return [graph_x, graph_y]
}

/**
 * JS doesnt have tuples.
 * @param t a string representation of a tuple  e.g. "(2, 4.3"
 * @returns the tuple converted to a list       e.g. [2, 4.3]
 */
export function parseTuple(t) {
    return JSON.parse("[" + t.replace(/\(/g, "[").replace(/\)/g, "]") + "]")[0];
}