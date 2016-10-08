var init = (target, backend) => {
	// Use target as the parent element to the vcs canvas
	var parent = document.querySelector(target);
	// Empty out the children
	while (parent.hasChildNodes()) {
		parent.removeChild(parent.firstChild);
	}
	var be = require("./vtk_websocket.js");
	return be.prepCanvas(parent);
}

module.exports = {"init": init};