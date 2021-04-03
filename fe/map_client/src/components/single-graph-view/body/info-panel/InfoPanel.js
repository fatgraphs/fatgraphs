import * as React from "react";
import DescriptionTable from "../../../description-table/DescriptionTable";

class InfoPanel extends React.Component {
    render() {
        return <div className={'border flex-3'}>
            <DescriptionTable
                    keys={['node info test hello:', 'test key:']}
                    values={["hello world", "test value"]}>
            </DescriptionTable>
        </div>
    }
}

export default InfoPanel