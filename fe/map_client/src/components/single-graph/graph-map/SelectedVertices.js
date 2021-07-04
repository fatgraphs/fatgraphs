import {draw_text_label, make_marker_with_popup, removeElement} from "../../../utils/Utils";
import {to_map_coordinate} from "../../../utils/CoordinatesUtil";

class SelectedVertices {
    /**
     * Class to manage the vertices selected via the search bar
     * @param map
     * @param graph_metadata
     * @param vertices_metadata
     */

    constructor(map, graph_metadata, vertices_metadata) {
        this.map = map;
        this.graph_metadata = graph_metadata;
        this.vertices_metadata = vertices_metadata;

        this.selected_vertices_markers = []
        this.selected_vertices_text_labels = []
    }


    update(zoom, selected_types) {
        for (const m in this.selected_vertices_markers) {
            removeElement(this.selected_vertices_markers[m], this.map);
        }
        for (const m in this.selected_vertices_text_labels) {
            removeElement(this.selected_vertices_text_labels[m], this.map);
        }
        this.selected_vertices_markers = [];
        this.selected_vertices_text_labels = [];

        let to_display = this.vertices_metadata
            .filter(vm => {
                let vertex_types = vm['types'].flat();
                return vertex_types.some(typ => selected_types.includes(typ))
            })

        for (let i in to_display) {
            const {pos, types, eth, size, labels} = to_display[i]

            let map_coordinate = to_map_coordinate(pos, this.graph_metadata)

            let label = draw_text_label(eth, map_coordinate, labels, types);
            label.addTo(this.map);

            let marker = make_marker_with_popup(
                'labelled-vertex-marker',
                map_coordinate,
                eth,
                labels,
                types,
                [size * 2 * (2 ** zoom),
                    size * 2 * (2 ** zoom)
                ])

            marker.addTo(this.map)
            this.selected_vertices_markers.push(marker)
            this.selected_vertices_text_labels.push(label)
        }
    }
}

export default SelectedVertices;