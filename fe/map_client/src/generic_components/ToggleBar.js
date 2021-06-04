import React, {Component} from 'react';
import SingleToggle from "./SingleToggle";

class ToggleBar extends Component {

    constructor(props) {
        super(props);
    }

    /**
     * A list of toggle that execute the attached callback
     * @returns {JSX.Element}
     */
    render() {
        return <div>
            {React.Children.map(this.props.children || null, (child, i) => {
                return <SingleToggle text={child.props.children} callback={child.props.callback}/>;
            })}
        </div>
    }
}

export default ToggleBar;