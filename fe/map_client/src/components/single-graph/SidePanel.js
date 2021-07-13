import * as React from "react";
import DescriptionTable from "../../generic_components/DescriptionTable";
import ToggleBar from "../../generic_components/ToggleBar";

class SidePanel extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {

        let address = this.props.addressDisplayedCurrently === undefined
            ? "Nothing selected"
            : this.props.addressDisplayedCurrently


        return <div className={'border-2'}>
            <DescriptionTable
                stackVertically={true}
                keys={['Address']}
                values={[address]}>
            </DescriptionTable>
        </div>
    }

}

export default SidePanel