import React, {Component} from 'react';
import SearchBar from "../searchBar/SearchBar";
import './tagBox.scss';
import './closeIcon.scss';
import './closeBox.scss';
import {TagElement} from "./tagElement";

class TagListGallery extends Component {

    constructor(props) {
        super(props);
        this.state = {
            tags: []
        }
        this.add = this.add.bind(this);
        this.removeWrapper = this.removeWrapper.bind(this);
    }



    render() {
        return (
            <div className={'d-flex flex-row flex-wrap'}>
                <SearchBar
                    placeholder={"Search graphs by name"}
                    searchCallback={this.add}/>
                    {this.state.tags.map((tag, i) =>
                        <TagElement
                            key={i}
                            closeCallback={this.removeWrapper(i)}>
                                <div>{tag}</div>
                        </TagElement>)}
            </div>
        );
    }

    add(tagObject) {
        let newTags = [...this.state.tags, tagObject];
        this.props.onChange(newTags);
        this.setState({tags: newTags});
    }

    removeWrapper(indexToRemove) {
        return function () {
            let tagsWithoutOne = [...this.state.tags.slice(0, indexToRemove), ...this.state.tags.slice(indexToRemove + 1, this.state.tags.length)];
            this.props.onChange(tagsWithoutOne)
            this.setState({tags: tagsWithoutOne})
        }.bind(this)
    }
}

export default TagListGallery;