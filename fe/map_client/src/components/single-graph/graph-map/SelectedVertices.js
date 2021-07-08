import {draw_text_label, make_marker_with_popup, removeElement} from "../../../utils/Utils";
import {to_map_coordinate} from "../../../utils/CoordinatesUtil";
import {fetch_matching_vertices} from "../../../API_layer";
import _ from 'underscore';

class SelectedVertices {
    /**
     * Class to manage the vertices selected via the search bar
     * @param map
     * @param graph_metadata
     * @param vertices_metadata
     */

    constructor(map, graph_metadata) {
        this.map = map;
        this.graph_metadata = graph_metadata;

        this.selected_vertices_markers = []
        this.selected_vertices_text_labels = []
    }


    async update(zoom, selected_tags) {
        for (const m in this.selected_vertices_markers) {
            removeElement(this.selected_vertices_markers[m], this.map);
        }
        for (const m in this.selected_vertices_text_labels) {
            removeElement(this.selected_vertices_text_labels[m], this.map);
        }
        this.selected_vertices_markers = [];
        this.selected_vertices_text_labels = [];

        let to_display = []

        for (const tag_object of selected_tags) {
            let response = await fetch_matching_vertices(this.graph_metadata.graph_name, tag_object);
            to_display.push(...response['response'])

            let grouped_by_eth = _.groupBy(to_display, 'eth');

            for (const eth in grouped_by_eth) {

                const types = grouped_by_eth[eth].map(obj => obj.type)
                const labels = grouped_by_eth[eth].map(obj => obj.label)

                const {pos, size} = grouped_by_eth[eth][0]

                let map_coordinate = to_map_coordinate(pos, this.graph_metadata)

                let text_label = draw_text_label(eth, map_coordinate, labels, types);
                text_label.addTo(this.map);

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
                this.selected_vertices_text_labels.push(text_label)
            }
        }
    }
}

export default SelectedVertices;