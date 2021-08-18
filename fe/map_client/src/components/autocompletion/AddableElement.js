import React, {Component} from 'react';
import * as PropTypes from "prop-types";
import {func, string} from "prop-types";
import {TYPE_ICONS} from "../single-graph/VisualElements";

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
                    this.props.onClick(this.props.metadata)
                }}
                onClick={() => {
                    this.props.onClick(this.props.metadata)
                }}>
                {TYPE_ICONS[this.props.metadata['type']]}
                { this.props.metadata['value']}
            </li>
        );
    }
}

AddableElement.propTypes = {
    bgColor: string,
    metadata: PropTypes.shape({
        value: string,
        type: PropTypes.oneOf(['label', 'type', 'eth']),
    }),
    onClick: func.isRequired,
};

AddableElement.defaultProps = {
    bgColor: 'odd:bg-white',
};

export default AddableElement;