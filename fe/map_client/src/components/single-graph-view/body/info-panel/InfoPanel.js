import * as React from "react";
import DescriptionTable from "../../../description-table/DescriptionTable";
import ToggleBar from "../toggle-bar/ToggleBar";
import SingleToggle from "../toggle-bar/SingleToggle";

class InfoPanel extends React.Component {
    render() {
        return <div className={'border-2'}>
            <ToggleBar>
                <span toggle={this.props.toggle[0]}>Toggle markers</span>
            </ToggleBar>
            <DescriptionTable
                    keys={['node info test hello:', 'test key:']}
                    values={["hello world", "test value"]}>
            </DescriptionTable>
        </div>
    }
}

export default InfoPanel