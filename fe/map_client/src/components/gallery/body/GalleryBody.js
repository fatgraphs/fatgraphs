import React, {Component} from 'react';
import GraphThumbnail from "./graph-thumbnail/GraphThumbnail";
import Modal from "../ModalMap";

class GalleryBody extends Component {

    constructor(props) {
        super(props);
        this.state = {
            available_graphs: props.available_graphs,
        }
    }

    componentDidMount() {

    }

    render() {
        return (
            <>
                <div className={'flex'}>
                    {this.state.available_graphs.map((value, index) => {
                        return <GraphThumbnail name={value} key={index}
                                               open_modal={this.openModal}
                                                close_modal={this.closeModal}/>
                    })}
                </div>
            </>
        );
    }
}

export default GalleryBody;