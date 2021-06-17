import React, {Component} from 'react';
import PropTypes from 'prop-types';

class SingleToggle extends Component {

    render() {
        return (
           <div className={'ml-1'}>
               <label>
                  <input
                    type="checkbox"
                    // checked={this.state.checked}
                    onChange={this.props.callback}
                  />
                  <span className={'ml-2'}>{this.props.text}</span>
                </label>
            </div>
        );
    }
}
SingleToggle.propsTypes = {
    callback: PropTypes.func.isRequired,
    text: PropTypes.string
}
export default SingleToggle;