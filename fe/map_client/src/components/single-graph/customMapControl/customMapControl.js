import L from 'leaflet';
import './customMapControl.css'

export default function makeCustomControl(callback, innerHTML, position) {
    let myCommand = L.Control.extend({

        onAdd: function (map) {

            let clickCallback = function () {
                this.options.callback()
            }.bind(this)

            var controlDiv = L.DomUtil.create('div');
            controlDiv.className += "leaflet-bar leaflet-control leaflet-control-clear";
            controlDiv.innerHTML = innerHTML;
            L.DomEvent
                .addListener(controlDiv, 'click', L.DomEvent.stopPropagation)
                .addListener(controlDiv, 'click', L.DomEvent.preventDefault)
                .addListener(controlDiv, 'click', callback);

            return controlDiv;
        }
    })
    return new myCommand({position: position})
}