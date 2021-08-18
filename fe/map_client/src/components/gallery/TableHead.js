import React from "react";

export class TableHead extends React.Component<{}> {

    render() {
        return <thead>
        <tr className="fs-sm">
            <th className="hidden-sm-down">#</th>
            <th>Preview</th>
            <th>Description</th>
            <th className="hidden-sm-down">Stats</th>
            <th className="hidden-sm-down">Date</th>
            <th className="hidden-sm-down">Zoom Levels</th>
        </tr>
        </thead>;
    }
}