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
                <dl>
                    {this.state.keys.map((value, index) => {
                    return <div key={index} className={'flex'}>
                        <dt>{value}</dt>
                        <dd className={'ml-2'}>{this.state.values[index]}</dd>
                    </div>;
                })}
                </dl>
            </div>
        );
    }
}

export default DescriptionTable;