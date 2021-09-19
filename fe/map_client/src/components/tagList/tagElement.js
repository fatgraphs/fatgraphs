import React, {Component} from "react"; import {TYPE_ICONS} from "../single-graph/TypeIcons";
export class TagElement extends Component {

    render() {
        return <div
            className={'d-flex flex-row'}
            key={this.props.key}>
            <div className={'tagBox'}>
                {this.props.children}

            </div>
            <div className={'closeBox'}
                 onClick={this.props.closeCallback}>
                <span className={'glyphicon glyphicon-remove closeIcon'}/>
            </div>
        </div>
  }
}