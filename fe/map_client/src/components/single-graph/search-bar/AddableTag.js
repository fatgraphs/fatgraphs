import React, {Component} from 'react';
import * as PropTypes from "prop-types";
import {func, string} from "prop-types";
import {type_to_icon} from "../../../utils/Utils";

class AddableTag extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        let tag_type = this.props.tag.tag_type;
        let tag_value = this.props.tag.tag;
        return (
            <li className={'flex flex-row ' + this.props.bg_color + ' dont-lose-focus'}
                tabIndex={0}
                onKeyDown={(e) => {
                    if (e.code.toLowerCase() !== 'enter') {
                        return;
                    }
                    this.props.addTagCallback(this.props.tag)
                }}
                onClick={() => {
                    this.props.addTagCallback(this.props.tag)
                }}>
                {type_to_icon[tag_type]}
                {tag_value}
            </li>
        );
    }
}

AddableTag.propTypes = {
    bg_color: string,
    term: PropTypes.shape({
        tag: string,
        tagType: PropTypes.oneOf(['label', 'type', 'eth']),
    }),
    addTagCallback: func.isRequired,
};

AddableTag.defaultProps = {
    bg_color: 'odd:bg-white',
};

export default AddableTag;