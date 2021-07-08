import React, {Component} from 'react';
import {bool, array, string} from "prop-types";
import AddableTag from "./AddableTag";
import {MyContext} from "../../../Context";

class Autocompletion extends Component {

    static contextType = MyContext

    constructor(props) {
        super(props);
        this.state = {
            autocomplete_terms: []
        }
    }

    componentDidMount() {
        let autocomplete_terms = this.context['autocomplete'];
        this.setState({
            autocomplete_terms: autocomplete_terms,
        })
    }

    render() {
        let regex = new RegExp('.*' + this.props.current_input.toLowerCase() + '.*');

        const matches = this.state.autocomplete_terms.filter(s => s['tag'].toLowerCase().match(regex));
        // we use the hidden  property to avoid re-building this long list (slow)
        return (
                <div
                    hidden={matches.length == 0 || ! this.props.visible}
                    className={'relative z-50'}>
                    <ul
                        className={'border-black border-2 p-2 flex flex-col absolute top-0 left-0 ml-1 bg-gray-100 w-48 h-48 overflow-y-auto'}>
                        {this.props.recentTags.map((term, i) => <AddableTag
                            key={i}
                            tag={term}
                            addTagCallback={this.props.addTagCallback}
                            bg_color={'bg-green-100'}/>)}
                        {matches.map((term, i) => <AddableTag
                            key={i + 5}
                            tag={term}
                            addTagCallback={this.props.addTagCallback}/>
                        )}
                    </ul>
                </div>
        );
    }
}

Autocompletion.propTypes = {
    current_input: string.isRequired,
    graph_name: string.isRequired,
    visible: bool.isRequired,
};

Autocompletion.defaultProps = {
    current_input: ''
};

export default Autocompletion;