import React, {Component} from 'react';

class DescriptionTable extends Component {
    constructor(props) {
        super(props);
        this.state = {
            keys: props.keys,
            values: props.values
        }
    }

    render() {
        return (
            <div>
                <dl className={'flex flex-row flex-wrap'}>
                    {this.state.keys.map((value, index) => {
                    return <div key={index} className={'flex flex-row mr-4 mt-4 odd:bg-gray-100'}>
                        <dt>{value}</dt>
                        <dd className={'ml-1'}>{this.state.values[index]}</dd>
                    </div>;
                })}
                </dl>
            </div>
        );
    }
}

export default DescriptionTable;