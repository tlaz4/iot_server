import React, { Component } from 'react';
import Settings from './Modal';
import ColorPicker from '@radial-color-picker/react-color-picker';


function hsvToRbg(h, s, l){
	 var r, g, b;

    if(s == 0){
        r = g = b = l; // achromatic
    }else{
        var hue2rgb = function hue2rgb(p, q, t){
            if(t < 0) t += 1;
            if(t > 1) t -= 1;
            if(t < 1/6) return p + (q - p) * 6 * t;
            if(t < 1/2) return q;
            if(t < 2/3) return p + (q - p) * (2/3 - t) * 6;
            return p;
        }

        var q = l < 0.5 ? l * (1 + s) : l + s - l * s;
        var p = 2 * l - q;
        r = hue2rgb(p, q, h + 1/3);
        g = hue2rgb(p, q, h);
        b = hue2rgb(p, q, h - 1/3);
    }

    return [Math.round(r * 255), Math.round(g * 255), Math.round(b * 255)];
}

function rbgToHsv(r, g, b){
	r /= 255, g /= 255, b /= 255;
    var max = Math.max(r, g, b), min = Math.min(r, g, b);
    var h, s, l = (max + min) / 2;

    if(max == min){
        h = s = 0; // achromatic
    }else{
        var d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        switch(max){
            case r: h = (g - b) / d + (g < b ? 6 : 0); break;
            case g: h = (b - r) / d + 2; break;
            case b: h = (r - g) / d + 4; break;
        }
        h /= 6;
    }

    return [h, s, l];

}

class Home extends Component {
	constructor(){
		super();
		this.state = {
			rooms: [],
			modalOpen: false,
			hue: 90,
			saturation: 100,
			luminosity: 50,
			alpha: 1,
			curDevice: null,
			curIdx: null,
			curRoomIdx: null
		}
		this.handleStatusChange = this.handleStatusChange.bind(this);
		this.handleModalOpen = this.handleModalOpen.bind(this);
		this.handleColorChange = this.handleColorChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
	}

	componentDidMount(){
		fetch('/api/rooms')
		.then(results => {
			return results.json();
		}).then(data => {
			if(data.status == 'success'){
				this.setState({ rooms: data.data.rooms});
			}
			console.log('fetching');
		});
	}

	handleStatusChange(event, devidx, roomidx){
		let data = {status: !this.state.rooms[roomidx].devices[devidx].status};
		let id = this.state.rooms[roomidx].devices[devidx].id;

		fetch('/api/devices/' + id, {
			method: 'PATCH',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(data),
		}).then(results => {
			return results.json();
		}).then(data => {
			if(data.status == 'success'){
				console.log('success');
				const obj = this.state.rooms.slice();
				obj[roomidx].devices[devidx] = data.data;
				this.setState({rooms: obj})
			}
		});
	}

	handleModalOpen(event, devidx, roomidx){
		event.preventDefault();
		if(!this.state.modalOpen){
			let curDevice = this.state.rooms[roomidx].devices[devidx];
			let hue = rbgToHsv(curDevice.red, curDevice.green, curDevice.blue)[0] * 360;
			this.setState({modalOpen: true, curIdx: devidx, curDevice: curDevice, curRoomIdx: roomidx, hue: hue})
		}else{
			this.setState({modalOpen: false, curIdx: null, curDevice: null, curRoomIdx: null})	
		}
		
	}

	handleColorChange(event){
		this.setState({hue: event.hue})
	}

	handleSubmit(event){
		let rgb = hsvToRbg(this.state.hue / 360, this.state.saturation / 100, this.state.luminosity / 100)
		console.log(rgb);
		let data = {red: rgb[0], green: rgb[1], blue: rgb[2]};
		let id = this.state.curDevice.id;

		fetch('/api/devices/' + id, {
			method: 'PATCH',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(data),
		}).then(results => {
			return results.json();
		}).then(data => {
			if(data.status == 'success'){
				console.log('success');
				const obj = this.state.rooms.slice();
				obj[this.state.curRoomIdx].devices[this.state.curIdx] = data.data;
				this.setState({rooms: obj, modalOpen: false, curIdx: null, curDevice: null, curRoomIdx: null})
			}
		});

	}

	render() {
		return (
			<div className="roomContainer">
				<div id="according">
				{this.state.rooms.map((room, roomidx) => (
					<div className="card">
					  <div className="card-header" id={"heading" + room.id}>
					    <h5 className="mb-0">
					      <button 
					      	className="btn btn-link"
					      	data-toggle="collapse"
					      	data-target={"#collapse" + room.id}
					      	aria-expanded="true"
					      	aria-controls={"collapse" + room.id}
					      >
					        <h5>{room.room_name}</h5>
					      </button>
					    </h5>
					  </div>

					  <div 
					  	id={"collapse" + room.id}
					  	class="collapse show" 
					  	aria-labelledby={"heading" + room.id} 
					  	data-parent="#accordion">
					  	<div class="card-body" style={{paddingTop: '0em'}}>
					  	{room.devices.map((device, devidx) => (
					  	 	<ul>
					  	 	  <li key={device.id}>
							  	  <div class="row align-items-center rowBottom">
							  	  	<div class="col-2">
							  	  	  	<i 
							  	  	  	  class="Material-icons icon" 
							  	  	  	  id="radio" 
							  	  	  	  style={{
							  	  	  	  	fontSize: '250%', 
							  	  	  	  	color: device.status ? '#007bff' : '#ccc'
							  	  	  	  }}
							  	  	  	>
							  	  	  	  radio
							  	  	  	</i>
							  	  	</div>
							  	  	<div class="col-5">
							  	  	  <h6>{device.device_name}</h6>
							  	  	</div>
							  	  	<div class="col-2">
							  	  	  <label class="switch">
									      <input 
									      	id="lcheck" type="checkbox" 
									      	defaultChecked={device.status}
									      	onChange={ (event) => this.handleStatusChange(event, devidx, roomidx)}
									      >
									      	</input>
									      <span class="slider round"></span>
									    </label>
							  	  	</div>
							  	  	<div class="col-3" style={{paddingBottom: '0.5em'}}>
							  	  	  <button 
							  	  	    type="button" 
							  	  	    class="btn btn-outline-primary" 
							  	  	    onClick={(event) => this.handleModalOpen(event, devidx, roomidx)}
							  	  	  >
							  	  	    Settings
							  	  	  </button>
							  	  	</div>
								  </div>
							  </li>
							</ul>
					  	))}
					  	</div>
					  </div>
					</div>
				))}
				</div>
				  <Settings 
				    open={this.state.modalOpen}
				    hue={this.state.hue}
				    saturation={this.state.saturation}
				    luminosity={this.state.luminosity}
				    alpha={this.state.alpha}
				    handleColorChange={this.handleColorChange}
				    handleClose={this.handleModalOpen}
				    handleSubmit={this.handleSubmit}
				  />
			</div>
		)
	}
}

export default Home;