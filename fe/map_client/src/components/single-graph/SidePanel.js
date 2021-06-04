import * as React from "react";
import DescriptionTable from "../../generic_components/DescriptionTable";
import ToggleBar from "../../generic_components/ToggleBar";

class SidePanel extends React.Component {

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
                <span callback={this.props.toggle[0]}>Toggle markers</span>
            </ToggleBar>
            <DescriptionTable
                stack_vertically={true}
                keys={['Address', "Label"]}
                values={[address, label]}>
            </DescriptionTable>
        </div>
    }

}

export default SidePanel