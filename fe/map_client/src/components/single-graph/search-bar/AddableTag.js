import React, {Component} from 'react';

class AddableTag extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div
                tabIndex={0}
                className={'z-50 odd:bg-white dont-lose-focus'}
                onKeyDown={(e) => {
                    if(e.code.toLowerCase() !== 'enter'){
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

export default AddableTag;