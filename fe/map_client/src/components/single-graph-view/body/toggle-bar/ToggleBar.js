import React, {Component} from 'react';
import SingleToggle from "./SingleToggle";

class ToggleBar extends Component {

    constructor(props) {
        super(props);
        this.state = {
            checked: props.is_marker_visible,
            call_back: props.call_back
        }
    }

    render() {
        return <div>
            {React.Children.map(this.props.children || null, (child, i) => {
                return <SingleToggle text={child.props.children} toggle={child.props.toggle}/>;
            })}
        </div>
    }
}

export default ToggleBar;