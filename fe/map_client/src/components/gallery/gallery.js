import React, {Component} from 'react';
import GalleryHeader from "./header/GalleryHeader";
import GalleryBody from "./body/GalleryBody";
import Modal from "./ModalMap";

const configs = require("configurations")

class Gallery extends Component {

    constructor() {
        super();
        this.state = {
            available_graphs: undefined,
        }
    }

    componentDidMount() {
        fetch(configs['endpoints']['base'] + configs['endpoints']['available_graphs'])
            .then(response =>
                response.json())
            .then(data => {
                this.setState({"available_graphs": data})
            })
    }


    render() {
        return this.state.available_graphs ?
            <div>
                <GalleryHeader/>
                <GalleryBody available_graphs={this.state.available_graphs}
                             className={"flex-1"}/>
            </div> :
            <div>Loading . . .</div>
    }
}

export default Gallery;