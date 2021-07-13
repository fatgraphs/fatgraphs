import * as React from "react";
import DescriptionTable from "../../generic_components/DescriptionTable";

class SidePanel extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {

        let address = this.props.addressDisplayedCurrently === undefined
            ? "Nothing selected"
            : this.props.addressDisplayedCurrently


        return<DescriptionTable
                className={this.props.className}
                stackVertically={true}
                keys={['Address']}
                values={[address]}>
            </DescriptionTable>
    }

}

export default SidePanel