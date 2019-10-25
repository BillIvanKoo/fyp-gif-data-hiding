import React from 'react';
import { Container, Row, Col, Tabs, Tab, Navbar } from 'react-bootstrap';

import GifEncode from './components/GifEncode';
import GifDecode from './components/GifDecode';

function App() {
  return (
    <div className="App">
      <Container>
        <Row>
          <Col>
            <Navbar>
              <Navbar.Brand>
                Data Hiding for GIF using Least Significant Byte
              </Navbar.Brand>
            </Navbar>
          </Col>
        </Row>
        <Row>
          <Col>
            <Tabs defaultActiveKey="encode">
              <Tab eventKey="encode" title="Encode">
                <GifEncode/>
              </Tab>
              <Tab eventKey="decode" title="Decode">
                <GifDecode/>
              </Tab>
            </Tabs>  
          </Col>  
        </Row>        
      </Container>
    </div>
  );
}

export default App;
