import React, {Component} from 'react';
import {TYPE_ICONS} from "../graph-map/VisualElements";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faTimesCircle} from "@fortawesome/free-regular-svg-icons";


class ClosableElement extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className={'border-black m-1 border-2 p-2 flex flex-row items-stretch relative z-50'}
                 onClick={() => {
                     this.props.closeCallback(this.props.metadata)
                 }}>

                {TYPE_ICONS[this.props.metadata['metadata_type']]}

                <div
                    className={'mr-3'}>{this.props.metadata['metadata_value']}</div>

                <FontAwesomeIcon
                    className={'text-red-500 text-2xl'}
                    icon={faTimesCircle}/>

            </div>
        );
    }
}

export default ClosableElement;