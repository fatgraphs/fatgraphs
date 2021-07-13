import React, {Component} from 'react';

class LabelVertex extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className={'border-black border-2 opacity-70 bg-white w-auto inline-block'}>
                <div className={'p-1 m-auto'}>{this.props.label}</div>
            </div>
        );
    }
}

export default LabelVertex;