import React, {Component} from 'react';
import DescriptionTable from "../../description-table/DescriptionTable";

class GraphMapHeader extends Component {

    constructor(props) {
        super(props);
        this.state = {
            nodes: props.graph_metadata.vertices,
            edges: props.graph_metadata.edges
        }
    }

    render() {
        return (
            <div>
                <h3 className={'text-2xl'}>Graph summary:</h3>
                <DescriptionTable
                    keys={['nodes', 'edges']}
                    values={[this.state.nodes, this.state.edges]}>
                </DescriptionTable>
            </div>
        );
    }
}

export default GraphMapHeader;