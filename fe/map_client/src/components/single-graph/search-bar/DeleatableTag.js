import React, {Component} from 'react';

class DeleatableTag extends Component {

    constructor(props) {
        super(props);
        this.remove = this.remove.bind(this)
    }

    render() {
        return (
            <div className={'border-black ml-1 border-2 p-2 flex flex-row items-center relative'}
                 onClick={this.remove}>
                <div className={'absolute -top-3 -right-3 h-5 w-5 leading-4 justify-center mr-1 border-red-600 border-2 bg-red-100 text-center'}>x</div>
                <span>{this.props.tag}</span>
            </div>
        );
    }

    remove(){
        this.props.closeCallback(this.props.tag)
    }
}

export default DeleatableTag;