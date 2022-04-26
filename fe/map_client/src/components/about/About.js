import React, {Component} from 'react';

class About extends Component {

    render() {
        return (
            <div class="about">
                <h1>About</h1>
                <p>This is a visualization tool that allows for the interactive exploration of potentially large graphs. It is still work in progress, and was built by Carlo Segat and Friedhelm Victor</p>
                <p>It makes use of the following technologies:</p>
                <ul>
                    <li>React.js</li>
                    <li>Leaflet maps</li>
                    <li>CuGraph</li>
                </ul>
                <p>It is not publically released yet, but will soon be available on GitHub. We will point this subdomain the corresponding repository in the future.</p>
            </div>
        );
    }
}

export default About;