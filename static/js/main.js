(() => {

"use strict";

const request = new XMLHttpRequest();
const attachButton = document.getElementById("attach-button");
const detachButton = document.getElementById("detach-button");

function makeRequest(command) {
	request.open("GET", `/${command}`);
	request.send();
}

window.addEventListener("load", _ => {
	attachButton.addEventListener("click", _ => makeRequest("attach"));
	detachButton.addEventListener("click", _ => makeRequest("detach"));
});

})();
