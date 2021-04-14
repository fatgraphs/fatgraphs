import React, {Component} from 'react';

class SingleToggle extends Component {
    render() {
        return (
           <div className={'ml-2'}>
               <label>
                  <input
                    type="checkbox"
                    // checked={this.state.checked}
                    onChange={this.props.toggle}
                  />
                  <span className={'ml-2'}>{this.props.text}</span>
                </label>
            </div>
        );
    }
}

export default SingleToggle;