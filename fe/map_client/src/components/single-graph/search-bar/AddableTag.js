import React, {Component} from 'react';
import {func, string} from "prop-types";

class AddableTag extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div
                tabIndex={0}
                className={this.props.bg_color + ' dont-lose-focus'}
                onKeyDown={(e) => {
                    if (e.code.toLowerCase() !== 'enter') {
                        return;
                    }
                    this.props.addTagCallback(this.props.tag)
                }}
                onClick={() => {
                    this.props.addTagCallback(this.props.tag)
                }}>
                {this.props.tag}
            </div>
        );
    }
}

AddableTag.propTypes = {
    bg_color: string,
    tag: string.isRequired,
    addTagCallback: func.isRequired,
};

AddableTag.defaultProps = {
    bg_color: 'odd:bg-white'
};

export default AddableTag;