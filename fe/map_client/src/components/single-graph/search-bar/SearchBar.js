import React, {Component} from 'react';
import DeleatableTag from "./DeleatableTag";
import Autocompletion from "./Autocompletion";
import {post_recent_tag} from "../../../API_layer";
import {MyContext} from "../../../Context";
import _ from 'underscore';

class SearchBar extends Component {

    static contextType = MyContext

    constructor(props) {
        super(props);
        this.state = {
            tags_selected: [],
            current_input: "",
            showAutocompletion: false,
            search_input_element: undefined
        }
        this.closeTagCallback = this.closeTagCallback.bind(this)
        this.addTagCallback = this.addTagCallback.bind(this)
        this.handleChange = this.handleChange.bind(this)
        this.onFocus = this.onFocus.bind(this)
        this.onBlur = this.onBlur.bind(this)
    }

    render() {
        return (
            <div className={'flex flex-row flex-wrap position-relative h-12'}>

                {/* DISPLAY SELECTED TAGS */}
                {this.state.tags_selected
                    .map((tag, i) =>
                        <DeleatableTag
                            tag={tag}
                            closeCallback={this.closeTagCallback}
                            key={i}/>
                    )}


                {/* this logic is to deal with the user pressing enter
                as opposed to the user clicking on the item they want to add*/}
                <form

                    onSubmit={() => {
                        let currentInput = this.state.current_input;
                        if(currentInput.substring(0, 2) === '0x'){
                            this.addTagCallback({
                                tag: currentInput,
                                tag_type: 'eth'})
                            return
                        }
                        if (this.context['types'].includes(currentInput)) {
                            this.addTagCallback({
                                tag: currentInput,
                                tag_type: 'type'})
                            return
                        }
                        if (this.context['labels'].includes(currentInput)) {
                            this.addTagCallback({
                                tag: currentInput,
                                tag_type: 'label'})
                            return
                        }
                        this.setState({
                            current_input: '',
                            showAutocompletion: false
                        })
                        this.state.search_input_element.blur()
                    }}
                    onBlur={this.onBlur}
                    className={'h-12 w-60'}>
                    <label>
                        <input className={'p-2 focus:outline-none'}
                               ref={inputEl => (this.state.search_input_element = inputEl)}
                               placeholder={'SEARCH BY NODE TYPE/LABEL'}
                               type="text"
                               value={this.state.current_input}
                               onChange={this.handleChange}
                               onFocus={this.onFocus}
                        />
                    </label>

                    <Autocompletion
                        visible={this.state.showAutocompletion} //this.state.showAutocompletion
                        current_input={this.state.current_input}
                        addTagCallback={this.addTagCallback}
                        graph_name={this.props.graph_name}
                        recentTags={this.props.recentTags}
                    />
                </form>
            </div>
        );
    }

    handleChange(event) {
        this.setState({current_input: event.target.value})
    }

    addTagCallback(tag_object) {
        this.setState(oldState => {
            this.state.search_input_element.blur()
            let tags_now = [...oldState.tags_selected, tag_object];

            // Update the quicklist
            if (!this.props.recentTags.some(t => _.isEqual(t, tag_object))) {
                post_recent_tag(tag_object)
            }

            // Update parent component
            this.props.set_selected_tags(tags_now)

            return ({
                tags_selected: tags_now,
                current_input: '',
                showAutocompletion: false
            });
        })

    }


    closeTagCallback(tag_object) {
        let tags_now = this.state.tags_selected.filter(tag => ! _.isEqual(tag, tag_object));
        this.setState({tags_selected: tags_now})
        this.props.set_selected_tags(tags_now)
    }

    onBlur(e) {
        if (e.relatedTarget !== null && e.relatedTarget.className.includes('dont-lose-focus')) {
            return
        }
        setTimeout(function () {
            this.setState({
                showAutocompletion: false
            })
        }.bind(this), 50)
    }

    onFocus(e) {
        this.setState({
            showAutocompletion: true
        })
    }
}

export default SearchBar;