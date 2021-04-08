import React, {Component} from 'react';
import DescriptionTable from "../../description-table/DescriptionTable";

class GraphMapHeader extends Component {

    constructor(props) {
        super(props);
        this.state = {
            nodes: props.graph_metadata.vertices,
            edges: props.graph_metadata.edges,
            median_distance: props.graph_metadata.median_distance
        }
    }

    render() {
        return (
            <div className={'border-2 lg:flex-1'}>
                <h3 className={'text-2xl'}>Graph summary:</h3>
                <DescriptionTable
                    keys={['nodes', 'edges', 'median_distance']}
                    values={[this.state.nodes, this.state.edges, this.state.median_distance]}>
                </DescriptionTable>
            </div>
        );
    }
}

export default GraphMapHeader;