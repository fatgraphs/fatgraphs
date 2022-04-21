import React, {Component} from 'react';
import noUiSlider from 'nouislider';
import 'nouislider/dist/nouislider.css';
import './slider-container.scss';
import * as PropTypes from "prop-types";
import wNumb from "wnumb";

class Sliders extends Component {

    constructor(props) {
        super(props);
        this.state = {
            vertexSlider: undefined,
            edgeSlider: undefined
        }
        this.sendValues = this.sendValues.bind(this);
    }

    componentDidMount() {

        let vertexSlider = this.createVertexSlider();
        let edgeSlider = this.createEdgeSlider();

        this.setState({
            vertexSlider: vertexSlider,
            edgeSlider: edgeSlider
        })
        vertexSlider.noUiSlider.on('update', this.sendValues);
        edgeSlider.noUiSlider.on('update', this.sendValues);

        setTimeout(this.sendValues, 50);
    }

    createEdgeSlider() {
        let edgeSlider = document.getElementById('edge-count');
        noUiSlider.create(edgeSlider, {
            start: [1, 10 ** 6],
            tooltips: false,
            connect: true,
            step: 10,
            range: {
                'min': [0, 100], 
                '25%': [1000, 100],
                '50%': [10000, 1000],
                '75%': [100000, 10000],
                'max': [1000000]
            },
            format: wNumb({
                decimals: 0
            }),
            pips: {
                mode: 'range',
                density: 5
            }
        });

        return edgeSlider;
    }

    createVertexSlider() {
        let vertexSlider = document.getElementById('vertex-count');

        noUiSlider.create(vertexSlider, {
            start: [1, 10 ** 6],
            tooltips: false,
            connect: true,
            step: 10,
            range: {
                'min': [0, 100], 
                '25%': [1000, 100],
                '50%': [10000, 1000],
                '75%': [100000, 10000],
                'max': [1000000]
            },
            format: wNumb({
                decimals: 0
            }),
            pips: {
                mode: 'range',
                density: 5
            }
        });


        return vertexSlider;
    }

    sendValues() {
        if (!this.state.vertexSlider || !this.state.edgeSlider) {
            return;
        }
        const vertices = this.state.vertexSlider.noUiSlider.get();
        const edges = this.state.edgeSlider.noUiSlider.get();
        console.log("sending values")
        this.props.updateCallback({
            vertices: vertices,
            edges: edges
        });

    }

    render() {
        return (
            <div className={'slider-container'}>
                <h3>Vertices</h3>
                <div className={'tg-slider'}
                     id="vertex-count"></div>

                <h3>Edges</h3>
                <div className={'tg-slider'}
                     id="edge-count"></div>
            </div>
        );
    }
}

Sliders.propTypes = {
    updateCallback: PropTypes.func
}

export default Sliders;