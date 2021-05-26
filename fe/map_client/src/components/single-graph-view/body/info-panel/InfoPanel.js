import * as React from "react";
import DescriptionTable from "../../../description-table/DescriptionTable";
import ToggleBar from "../toggle-bar/ToggleBar";
import SingleToggle from "../toggle-bar/SingleToggle";

class InfoPanel extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {

        let address = this.props.address_displayed_currently === undefined
            ? "Nothing selected"
            : this.props.address_displayed_currently[1]

        let label = this.props.address_displayed_currently === undefined
            ? ""
            : this.props.address_displayed_currently[0]

        return <div className={'border-2'}>
            <ToggleBar>
                <span toggle={this.props.toggle[0]}>Toggle markers</span>
            </ToggleBar>
            <DescriptionTable
                stack_vertically={true}
                keys={['Address', "Label"]}
                values={[address, label]}>
            </DescriptionTable>
        </div>
    }

}

export default InfoPanel