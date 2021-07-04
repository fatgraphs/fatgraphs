import {to_map_coordinate} from "../../../utils/CoordinatesUtil";
import {make_marker_with_popup, removeElement} from "../../../utils/Utils";

class ClickClosestVertex {
    /**
     * Class to manage the marker placed on the vertex that is closer to the clicked spot on the map.
     * This we refer to as the "proximity-click" mechanism.
     * @param map
     * @param graph_metadata
     */

    constructor(map, graph_metadata) {
        this.map = map;
        this.graph_metadata = graph_metadata;

        this.closest_vertex_marker = undefined;
    }

    update(zoom, closest_vertex) {
        if (closest_vertex === undefined) {
            return;
        }

        if (this.closest_vertex_marker !== undefined) {
            removeElement(this.closest_vertex_marker, this.map);
        }

        let graphCoordinate = [Number.parseFloat(closest_vertex['x']), Number.parseFloat(closest_vertex['y'])];
        let pos = to_map_coordinate(graphCoordinate, this.graph_metadata)
        let types = closest_vertex['types']
        let labels = closest_vertex['labels']

        let marker2 = make_marker_with_popup(
            'proximity-marker',
            pos,
            closest_vertex['eth'],
            labels,
            types,
            [closest_vertex['size'] * (2 ** zoom),
                closest_vertex['size'] * (2 ** zoom)
            ])

        marker2.addTo(this.map);

        this.closest_vertex_marker = marker2;
    }
}

export default ClickClosestVertex;