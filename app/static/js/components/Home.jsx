import React, { Component } from 'react';

class Home extends Component {
	constructor(){
		super();
		this.state = {
			rooms: [],
		}
		this.handleStatusChange = this.handleStatusChange.bind(this);
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
							  	  	  <button type="button" class="btn btn-outline-primary">Settings</button>
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
			</div>
		)
	}
}

export default Home;