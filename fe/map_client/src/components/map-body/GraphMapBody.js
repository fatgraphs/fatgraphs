import React from "react";
import Mymap from "./graph-map/Mymap";
import InfoPanel from "./info-panel/InfoPanel";

class GraphMapBody extends React.Component {
    render() {
        return <div className={'container flex'}>
            <Mymap/>
            <InfoPanel/>
        </div>
    }
}

export default GraphMapBody