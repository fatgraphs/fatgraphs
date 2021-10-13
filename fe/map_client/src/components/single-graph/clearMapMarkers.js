import L from 'leaflet';
import './clearMapMarkersControl.css'


L.Control.Command = L.Control.extend({

    onAdd: function (map) {

        let clickCallback = function () {
                this.options.callback()}.bind(this)

        var controlDiv = L.DomUtil.create('div');
        controlDiv.innerHTML = `
            <div>
              <button>Clear</button>
            </div>`;
        L.DomEvent
            .addListener(controlDiv, 'click', L.DomEvent.stopPropagation)
            .addListener(controlDiv, 'click', L.DomEvent.preventDefault)
            .addListener(controlDiv, 'click', clickCallback);

        return controlDiv;
    }
});

L.control.clearMapMarkersControl = function (options) {
    options['position'] = 'bottomleft'
    return new L.Control.Command(options);
};
