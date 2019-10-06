import React, { Component } from 'react'
import { Form, Image, Button } from 'react-bootstrap'

class GifDecode extends Component {
    constructor(props){
        super(props);
        this.state = {
            selectedFile: null,
            preview: null,
            message: ""
        }
    }

    handleGifSubmit(e) {
        e.preventDefault();

        const data = new FormData()
        data.append('file', this.state.selectedFile)

        fetch('http://localhost:5000/gif/decode', {
            method: 'POST',
            body: data
        }).then((res)=>{
            res.json().then(body => {
                this.setState({
                    message: body.message
                })
            })
        })
       
        
    }

    render() {
        return (
            <Form>
                <Form.Group>
                <Form.Control type="file" placeholder="select GIF" onChange={(e)=>{
                    this.setState({
                        selectedFile: e.target.files[0],
                        preview: URL.createObjectURL(e.target.files[0])
                    })
                }}/>
                <Image src={this.state.preview}/>
                </Form.Group>
                <Button type="submit" onClick={(e)=>{this.handleGifSubmit(e)}}>
                    Get Hidden Message
                </Button>
            </Form>
        )
    }
}

export default GifDecode;