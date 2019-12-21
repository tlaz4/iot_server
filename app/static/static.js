function radioPost(){
	radio = document.getElementById("radio");
	check = document.getElementById("rcheck")

	if(check.checked){
		radio.style.setProperty("color", "#ccc");
		postData("/radio", {status: "off"});
	}else if(!check.checked){
		radio.style.setProperty("color", "#2369B8");
		postData("/radio", {status: "on"});
	}
}

function lanternPost(){
	radio = document.getElementById("wb_incandescent");
	check = document.getElementById("lcheck")

	if(check.checked){
		radio.style.setProperty("color", "#ccc");
		postData("/lantern", {status: "off"});
	}else if(!check.checked){
		radio.style.setProperty("color", "#2369B8");
		postData("/lantern", {status: "on"});
	}
}

function postData(url, data){
	return fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type' : 'application/json',
		},
		body: JSON.stringify(data),
	})
	.then(res => res.json())
	.then(reponse => console.log(JSON.stringify(reponse)));
}

//#133863
