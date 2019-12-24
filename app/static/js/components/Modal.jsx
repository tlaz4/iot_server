import React from 'react';
import Dialog from '@material-ui/core/Dialog';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogActions from '@material-ui/core/DialogActions';
import ColorPicker from '@radial-color-picker/react-color-picker';

const Settings = (props) => {

	return(
		<div>
			<Dialog
			  open={props.open}
			  aria-labelledby='device-settings'
			  onClose={(event) => props.handleClose(event, null, null)}
			>
			  <DialogTitle id='device-settings-title'>
			    Device Settings
			  </DialogTitle>
			  <DialogContent>
			    <DialogContentText>
			      Control a devices settings here
			    </DialogContentText>
			    <div>
			      <ColorPicker 
				    hue={props.hue} 
				    saturation={props.saturation}
				    luminosity={props.luminosity}
				    alpha={props.alpha}
				    onChange={(event) => props.handleColorChange(event)}
				  />
			    </div>
			  </DialogContent>
			  <DialogActions>
			  	<button 
				  type="button" 
				  class="btn btn-outline-primary" 
				  onClick={(event) => props.handleSubmit(event)}
				>
				  Submit
				</button>
				<button 
				  type="button" 
				  class="btn btn-outline-primary" 
				  onClick={(event) => props.handleClose(event, null, null)}
				>
				  Close
				</button>

			  </DialogActions>
			</Dialog>
		</div>
	)
}

export default Settings;