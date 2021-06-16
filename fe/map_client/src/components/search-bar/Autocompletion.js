import React, {Component} from 'react';
import {bool, string} from "prop-types";
import AddableTag from "./AddableTag";
import {fetchVerticesMetadata} from "../../API_layer";

class Autocompletion extends Component {

    constructor(props) {
        super(props);
        this.state = {
            availableStrings: [],
        }
    }

    async componentDidMount() {
        let vertices_metadata = await fetchVerticesMetadata(this.props.graph_name)
        let map = Object.keys(vertices_metadata).map(key => vertices_metadata[key][0]);
        this.setState({availableStrings: map})
    }


        render()
        {
            let regex = new RegExp('.*' + this.props.current_input.toLowerCase() + '.*');
            const matchedStrings = this.state.availableStrings.filter(s => s.toLowerCase().match(regex));
            return (
                matchedStrings.length > 0 && this.props.visible ?
                    <div className={'relative'}>
                        <div
                            className={'border-black border-2 p-2 flex flex-col absolute top-0 left-0 ml-1 bg-gray-100 w-48 h-48 overflow-y-auto'}>
                            {matchedStrings.map((str, i) => <AddableTag
                                key={i}
                                tag={str}
                                addTagCallback={this.props.addTagCallback}/>
                            )}
                        </div>
                    </div> :
                    <div/>
            )
                ;
        }
    }

Autocompletion.propTypes = {
    current_input: string.isRequired,
    graph_name: string.isRequired,
    visible: bool.isRequired
};

Autocompletion.defaultProps = {
    current_input: ''
};


export default Autocompletion;