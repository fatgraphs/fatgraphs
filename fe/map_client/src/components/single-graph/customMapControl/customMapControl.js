import L from 'leaflet';
import './customMapControl.css'

export default function makeCustomControl(callback, innerHTML, position) {
    let myCommand = L.Control.extend({

        onAdd: function () {

            var controlDiv = L.DomUtil.create('div');
            controlDiv.className += "leaflet-bar leaflet-control leaflet-control-clear";
            controlDiv.innerHTML = innerHTML;

            // bug prevention: double-clicking a custom control should not make the map zoom
            controlDiv.ondblclick = (e) => {
                e.stopPropagation();
            };

            L.DomEvent
                .addListener(controlDiv, 'click', L.DomEvent.stopPropagation)
                .addListener(controlDiv, 'click', L.DomEvent.preventDefault)
                .addListener(controlDiv, 'click', callback);

            return controlDiv;
        }
    })
    return new myCommand({position: position})
}