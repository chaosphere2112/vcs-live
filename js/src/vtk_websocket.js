var onResize = require("element-resize-event");



module.exports = {
	prepCanvas: (parent) => {
		var c = document.createElement("canvas");
		parent.appendChild(c);
		c.width = parent.clientWidth;
		c.height = parent.clientHeight;

		var socket = new Promise(function(resolve, reject) {
			var ws = new WebSocket("ws://@@@SERVER@@@/canvas");
			ws.binaryType = "arraybuffer";
			ws.onopen = () => {
				console.log("Opened");
				resolve(ws);
				console.log("Resolved");
			}
		});

		var context = c.getContext("2d");

		var send = (obj) => {
			socket.then(function(ws){
				console.log("Sending text");
				ws.send(JSON.stringify(obj));
			});
		}

		send({"event": "resize", "width": c.width, "height": c.height})

		socket.then(function(ws) {
			ws.onmessage = (evt) => {
				console.log("Server responded");
				var buffer = new Uint8ClampedArray(evt.data);
				console.log(c.width, c.height);
				console.log(buffer.length)
				var img = new ImageData(buffer, c.width, c.height);
				context.putImageData(img, 0, 0);
			}
		});

		onResize(parent, ()=>{
			c.width = parent.clientWidth;
			c.height = parent.clientHeight;
			//send({"event": "resize", "width": c.width, "height": c.height});
		});

		
		return {
			"parent": parent,
			"canvas": c,
			"plot": (data, gm, tmpl) => {
				if (tmpl == undefined) {
					tmpl = null;
				}
				send({"event": "plot", "data": data, "gm": gm, "tmpl": tmpl});
			}
		}
	}
}