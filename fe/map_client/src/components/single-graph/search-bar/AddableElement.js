import React, {Component} from 'react';
import * as PropTypes from "prop-types";
import {func, string} from "prop-types";
import {TYPE_ICONS} from "../graph-map/VisualElements";

class AddableElement extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <li className={'flex flex-row ' + this.props.bgColor + ' dont-lose-focus'}
                tabIndex={0}
                onKeyDown={(e) => {
                    if (e.code.toLowerCase() !== 'enter') {
                        return;
                    }
                    this.props.addMetadataCallback(this.props.metadata)
                }}
                onClick={() => {
                    this.props.addMetadataCallback(this.props.metadata)
                }}>
                {TYPE_ICONS[this.props.metadata['metadata_type']]}
                { this.props.metadata['metadata_value']}
            </li>
        );
    }
}

AddableElement.propTypes = {
    bgColor: string,
    metadata: PropTypes.shape({
        metadataValue: string,
        metadataType: PropTypes.oneOf(['label', 'type', 'eth']),
    }),
    addMetadataCallback: func.isRequired,
};

AddableElement.defaultProps = {
    bgColor: 'odd:bg-white',
};

export default AddableElement;