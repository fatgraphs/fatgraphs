import React, {Component} from 'react';

class ToggleBar extends Component {

    constructor(props) {
        super(props);
        this.state = {
            checked: props.is_marker_visible,
            call_back: props.call_back
        }
    }
    render() {
        return (
            <div className={'border flex-6'}>
               <label>
                  <input
                    type="checkbox"
                    checked={this.state.checked}
                    onChange={this.state.call_back}
                  />
                </label>
            </div>
        );
    }
}

export default ToggleBar;