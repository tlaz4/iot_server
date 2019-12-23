import React from 'react';
import Routes from './routes';

function App(){
  return (
  	<div>
      <nav className="navbar navbar-light bg-light">
        <a className="navbar-brand" href="/">IOT</a>
      </nav>
      <div>
    	  <Routes />
      </div>
    </div>
  )
}

export default App;
