import React, {Component} from 'react';

const configs = require('configurations')

class GraphThumbnail extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return <>
            <div className={"m-2 p-1 border-1 border-white cursor-pointer hover:bg-gray-300 text-center"}
                 onClick={() => this.props.open(this.props.name)}>
                <img src={configs['endpoints']['base']+"/tokengallery/tile/"+this.props.name+"/0/0/0.png"}/>
                <p>{this.props.name}</p>
            </div>
        </>;
    }
}

export default GraphThumbnail;
