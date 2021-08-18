import * as React from "react";
import Static from "../../reactBlueTemplate/src/pages/tables/static/Static"

class SidePanel extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {

        return <>
            <Static
                title={'Selected Vertices'}
                closestVertex={this.props.closestVertex}
                selectedVertices={this.props.markersSelectedMetadata}/>
        </>
    }

}

export default SidePanel