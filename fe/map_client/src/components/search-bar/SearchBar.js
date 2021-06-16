import React, {Component} from 'react';
import DeleatableTag from "./DeleatableTag";
import Autocompletion from "./Autocompletion";

class SearchBar extends Component {

    constructor(props) {
        super(props);
        this.state = {
            tags_selected: [],
            current_input: "",
            showAutocompletion: false,
            searchInput: undefined
        }
        this.closeTagCallback = this.closeTagCallback.bind(this)
        this.addTagCallback = this.addTagCallback.bind(this)
        this.handleChange = this.handleChange.bind(this)
        this.onFocus = this.onFocus.bind(this)
        this.onBlur = this.onBlur.bind(this)
    }

    render() {
        return (
            <div className={'flex flex-row border-2 position-relative h-12 z-50'}>

                {this.state.tags_selected
                    .map((keyword, i) => <DeleatableTag
                        tag={keyword}
                        closeCallback={this.closeTagCallback}
                        key={i}>{keyword}</DeleatableTag>
                    )}


                <form
                    onSubmit={() => this.addTagCallback(this.state.current_input)}
                    onBlur={this.onBlur}
                    className={'h-12 w-60'}>
                    <label className={'ml-1'}>
                        <input className={'p-2 focus:outline-none'}
                               ref={inputEl => (this.searchInput = inputEl)}
                               placeholder={'insert tag'}
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
                    />
                </form>
            </div>
        );
    }

    handleChange(event) {
        console.log(event)
        this.setState({current_input: event.target.value})
    }

    addTagCallback(newTag) {
        this.setState(oldState => ({
            tags_selected: [...oldState.tags_selected, newTag],
            current_input: '',
            showAutocompletion: false
        }))
        // this.searchInput.focus();
    }


    closeTagCallback(toremove) {
        this.setState({tags_selected: this.state.tags_selected.filter(tag => tag !== toremove)})
    }

    onBlur(e) {
        if (e.relatedTarget !== null && e.relatedTarget.className.includes('dont-lose-focus')) {
            return
        }
        setTimeout(function () { //Start the timer
            this.setState({
                showAutocompletion: false
            })
        }.bind(this), 100)
    }

    onFocus(e) {
        this.setState({
            showAutocompletion: true
        })
    }
}

export default SearchBar;