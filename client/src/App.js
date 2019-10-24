import React from 'react';
import { Tabs, Tab } from 'react-bootstrap';

import GifEncode from './components/GifEncode';
import GifDecode from './components/GifDecode';

function App() {
  return (
    <div className="App">
      <Tabs defaultActiveKey="encode">
        <Tab eventKey="encode" title="Encode">
          <GifEncode/>
        </Tab>
        <Tab eventKey="decode" title="Decode">
          <GifDecode/>
        </Tab>
      </Tabs>
      
    </div>
  );
}

export default App;
