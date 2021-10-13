import L from 'leaflet';
import './testCustomControl.css'


L.Control.Command = L.Control.extend({
    options: {
        position: 'topleft',
    },


    callback :function (){
        console.log("Ciaooo")
    },

    onAdd: function (map) {

        let clickCallback = function () {
                console.log("ciao", this.options.callback);
                this.options.callback()}.bind(this)

        var controlDiv = L.DomUtil.create('div');
        controlDiv.innerHTML = `
            <div>
              <form>
                <input 
                    class="leaflet-control-layers-overlays map-checkbox" 
                    id="show-edges-command" 
                    type="checkbox">
                  edge overlay
                </input>
              </form>
            </div>`;
        L.DomEvent
            .addListener(controlDiv, 'click', L.DomEvent.stopPropagation)
            // .addListener(controlDiv, 'click', L.DomEvent.preventDefault)
            .addListener(controlDiv, 'click', clickCallback);

        return controlDiv;
    }
});

L.control.testControl = function (options) {
    return new L.Control.Command(options);
};

// console.log(">>>>, ", L.control.testControl)
