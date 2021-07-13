import React, {Component} from 'react';
import {TYPE_ICONS} from "../graph-map/VisualElements";


class ClosableMetadata extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className={'border-black ml-1 border-2 p-2 flex flex-row items-center relative'}
                 onClick={() => {
                     this.props.closeCallback(this.props.metadata)
                 }}>

                {TYPE_ICONS[this.props.metadata['metadata_type']]}

                {this.getCloseButton()}

                <span>{this.props.metadata['metadata_value']}</span>

            </div>
        );
    }

    getCloseButton() {
        return <div
            className={'absolute -top-3 -right-3 h-5 w-5 leading-4 justify-center mr-1 border-red-600 border-2 bg-red-100 text-center rounded-full'}>
            <div className={'relative -top-px  -top-px'}>
                x
            </div>
        </div>;
    }
}

export default ClosableMetadata;