import React, {Component} from 'react';

class LabelVertex extends Component {

    constructor(props) {
        super(props);
    }


    render() {
        return (
            <div className={'label-container'}>
                <span className={'label-vertex'}>{this.props.label}</span>
            </div>
        );
    }
}

export default LabelVertex;