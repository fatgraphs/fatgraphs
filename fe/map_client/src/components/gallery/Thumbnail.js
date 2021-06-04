import React, {Component} from 'react';

class GraphThumbnail extends Component {

    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this)
    }

    render() {
        return <>
            <div className={"m-2 p-1 border-4 border-black bg-gray-100 border-opacity-75 cursor-pointer hover:bg-gray-300"}
                 onClick={this.handleClick}>
                <p>{this.props.name}</p>
            </div>
        </>;
    }

    handleClick() {
        this.props.open(this.props.name)
    }
}

export default GraphThumbnail;