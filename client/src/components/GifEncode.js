import React from 'react'
import { Form, Button, Image } from 'react-bootstrap'

class GifEncode extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            selectedFile: null,
            capacity: null,
            preview: null,
            message: "",
            result_preview: null,
            result_blob: null
        }
    }

    handleGifSubmit(e) {
        e.preventDefault();

        const data = new FormData()
        data.append('file', this.state.selectedFile)
        data.append('message', this.state.message)

        if (this.state.capacity === null) {
            fetch('http://localhost:5000/gif/calculate', {
                method: 'POST',
                body: data
            }).then((res)=>{
                res.json().then(body => {
                    this.setState({
                        capacity: body.capacity
                    })
                })
            })
        } else {
            
            fetch('http://localhost:5000/gif/encode', {
                method: 'POST',
                body: data
            }).then((res) => {
                res.blob().then(blob => {
                    let tempURL = URL.createObjectURL(blob);
                    this.setState({
                        result_blob: blob,
                        result_preview: tempURL
                    })
                })
            })
        }
        
    }

    handleCapacity() {
        if (this.state.capacity === null) {
            return (
                <Button type="submit" onClick={(e)=>{this.handleGifSubmit(e)}}>
                    Calculate Capacity
                </Button>
            )
        } else {
            return (
                <>
                <h3>Capacity: {this.state.message.length}/{this.state.capacity} characters</h3>
                <Form.Group>
                    <Form.Control maxLength={this.state.capacity} as="textarea" rows="3" onChange={(e)=>{
                        this.setState({
                            message: e.target.value
                        })
                    }}/>
                </Form.Group>
                <Button type="submit" onClick={(e)=>{this.handleGifSubmit(e)}}>
                    Hide Text
                </Button>
                </>
            )
        }
    }

    handleResult() {
        if (this.state.result_preview === null) {
            return (<></>)
        } else {
            return (
                <>
                <h3>Result</h3>
                <Image src={this.state.result_preview}/>
                <Button as="a" href={this.state.result_preview} download="encoded.gif">Save Encoded Image</Button>
                
                </>
            )
        }
    }

    uploadGiphy(e) {
        e.preventDefault()
        let reader = new FileReader();
        reader.readAsBinaryString(this.state.result_blob)
        reader.onloadend = e => {
            fetch('//upload.giphy.com/v1/gifs?api_key=XyJkToB19lwALPJfJvs6KPQsrijQw0oM', {
                method: 'POST',
                headers: {'Content-Type':'application/json'},
                body: {
                    api_key: "XyJkToB19lwALPJfJvs6KPQsrijQw0oM",
                    file: reader.result
                }
            }).then(res => {
                res.json().then(body => {
                    fetch(`//api.giphy.com/v1/gifs/${body.response_id}?api_key=XyJkToB19lwALPJfJvs6KPQsrijQw0oM`, {
                        headers: {
                            api_key:"XyJkToB19lwALPJfJvs6KPQsrijQw0oM"
                        }
                    }).then((res)=>{
                        res.json(body => {
                            console.log(body)
                        })
                    })
                })
            })
        }
    }

    render() {
         return (
            <Form>
                <Form.Group>
                <Form.Control type="file" placeholder="select GIF" onChange={(e)=>{
                    if (e.target.files.length > 0){
                        this.setState({
                            selectedFile: e.target.files[0],
                            preview: URL.createObjectURL(e.target.files[0]),
                            capacity: null
                        })
                    }
                }}/>
                <Image src={this.state.preview}/>
                </Form.Group>
                {this.handleCapacity()}
                {this.handleResult()}
            </Form>
         )
    }
}

export default GifEncode