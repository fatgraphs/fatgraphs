import React, {Component} from 'react';
import Modal from "../../ModalMap";
import SingleGraphView from "../../../single-graph-view/SingleGraphView";

class GraphThumbnail extends Component {

    constructor(props) {
        super(props);
        this.state = {
            name: props.name,
            key: props.key,
            show_modal: false,
        }
        this.openModal = this.openModal.bind(this)
        this.closeModal = this.closeModal.bind(this)
    }

    render() {
        return <>
            <div key={this.state.key}
                 className={"m-2 p-1 border-4 border-black bg-gray-100 border-opacity-75 cursor-pointer hover:bg-gray-300"}
                 onClick={this.openModal}>
                <p>{this.state.name}</p>
            </div>
            {this.state.show_modal ?
                <Modal close_modal={this.closeModal}
                title={this.state.name}>
                   <SingleGraphView graph_name={this.state.name}/>
                </Modal>
                : null}
        </>;
    }

    openModal() {
        this.setState({show_modal: true})
    }

    closeModal() {
        this.setState({show_modal: false})
    }
}

export default GraphThumbnail;