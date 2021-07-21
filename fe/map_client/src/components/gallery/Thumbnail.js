import React, {Component} from 'react';
import UrlComposer from "../../utils/UrlComposer";

const configs = require('configurations')

class GraphThumbnail extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        let s = UrlComposer.tileLayer(this.props.graph['id'], 0, 0, 0);
        s = s.replace(/{randint}/g, 43);
        console.log(s)
        return <>
            <div className={"m-2 p-1 border-1 border-white cursor-pointer hover:bg-gray-300 text-center"}
                 onClick={() => this.props.open(this.props.graph)}>
                <img src={s}/>
                <p>{this.props.graph['graphName']}</p>
            </div>
        </>;
    }
}

export default GraphThumbnail;
