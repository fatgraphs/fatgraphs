import React from "react";
import GraphSummary from "./summary-info/GraphSummary";
let configs = require('configurations');

class GraphMapHeader extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            graph_name: props.graph_name,
            graph_summary: null
        }
    }

    componentDidMount() {
        fetch(configs['endpoints']['base'] + configs['endpoints']['graph_summary'])
            .then(response =>
                response.json())
            .then(data => {
                this.setState({"graph_summary": data})
            })
    }

    render() {
        if(this.state.graph_summary === null){
            return <div>Loading...</div>
        } else {
            return <header className={'border'}>
            <h2 className={'text-6xl'}>{this.state.graph_name}</h2>
            <GraphSummary nodes={this.state.graph_summary['nodes']}
                          edges={this.state.graph_summary['edges']}/>
        </header>;
        }
    }
}
export default GraphMapHeader