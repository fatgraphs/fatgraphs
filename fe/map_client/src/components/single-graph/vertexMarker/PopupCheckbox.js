import React, {Component} from 'react';
import * as PropTypes from "prop-types";

class PopupCheckbox extends Component {

    constructor(props) {
        super(props);
        this.state = {
            ticked: false
        }
    }


    render() {
        return (
            <div>
                <form>
                    <div className={"map-checkbox-container"}>
                        <label>
                            <input className={"map-checkbox-small"}
                                   id="persist-edges"
                                   type="checkbox"
                                   checked={this.props.ticked || this.state.ticked}
                                   onChange={(e) => {
                                       this.props.checkboxCallback(e)
                                       this.setState({ticked: true})
                                   }}>
                            </input>
                            <span>Persist</span>
                        </label>
                    </div>
                </form>
            </div>
        );
    }
}

PopupCheckbox.propTypes = {
    ticked: PropTypes.bool,
    checkboxCallback: PropTypes.func
}

export default PopupCheckbox;