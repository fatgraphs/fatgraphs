import React, {Component} from 'react';

const configs = require("configurations")

class EdgeDistributionViewer extends Component {

    constructor(props) {
        super(props);
        this.state = {
            imgs: [],
            allImgsFetched: false
        }
    }
    componentDidMount() {
        let fetches = []
        for (let zoom_level = 0; zoom_level < this.props.zoom_levels; zoom_level++) {
            let name_zoom = "/" + this.props.graph_name + "/" + zoom_level;
            fetches.push(fetch(configs['endpoints']['base'] + configs['endpoints']['edge_distributions'] + name_zoom)
                .then(response => {
                    return response.blob()
                })
                .then(data => {
                    this.setState({"imgs": [...this.state.imgs, data]})
                }));
        }
        Promise.all(fetches).then(result => {
            this.setState({allImgsFetched : true})
        })
    }

    render() {
        return this.state.allImgsFetched ?
            <div className={'flex flex-row flex-wrap'}>
                {this.state.imgs.map(img => {
                    return <img width={'500rem'} src={URL.createObjectURL(img)} />
                })}
            </div> :
            <div>Loading . . .</div>
    }
}

export default EdgeDistributionViewer;