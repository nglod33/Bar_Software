import axios from 'axios';
 
import React,{Component} from 'react';
 
class App extends Component {
  
    
    state = {
 
      // Initially, no file is selected
      selectedFile: null,
    };
    
    // On file select (from the pop up)
    onFileChange = event => {
    
      // Update the state
      this.setState({ selectedFile: event.target.files[0] });
    
    };

    
    // On click of the post license button
    onPostID = () => {
    
      // Create an object of formData
      const formData = new FormData();
    
      // Update the formData object
      formData.append(
        "file",
        this.state.selectedFile
      );
      
      formData.append("token", "sampleToken");
    
      // Details of the uploaded file
      console.log(this.state.selectedFile);
    
      // Request made to the backend api
      // Send formData object
      axios.post("http://localhost:8080/picture", formData)
      .then((response) => {this.setState({selectedResponse: response})});

    };

    // On click of the check license Button
    onCheckID = () => {
    
      // Create an object of formData
      const formData = new FormData();
    
      // Update the formData object
      formData.append(
        "file",
        this.state.selectedFile
      );
      
      formData.append("token", "sampleToken");
    
      // Details of the uploaded file
      console.log(this.state.selectedFile);
    
      // Request made to the backend api
      // Send formData object
      axios.get("http://localhost:8080/picture", formData)
      .then(function (response) {
        this.state.selectedResponse.setState(response.data);
      });
    }

    getResponse = () => {
      if (this.state.selectedResponse) {
        return (
          this.selectedResponse
        )
      }
      else{
        return (
          "No response yet"
        )
      }
    }
    
    // File content to be displayed after
    // file upload is complete
    fileData = () => {
    
      if (this.state.selectedFile) {
         
        return (
          <div>
            <h2>File Details:</h2>
             
<p>File Name: {this.state.selectedFile.name}</p>
 
             
<p>File Type: {this.state.selectedFile.type}</p>
 
          </div>
        );
      } else {
        return (
          <div>
            <br />
            <h4>Choose before Pressing the Upload button</h4>
          </div>
        );
      }
    };
    
    render() {
      const {
        selectedFile,
        selectedResponse
      } = this.state;
    
      return (
        <div>
            <h1>
              Scannr
            </h1>
            <h3>
              Upload File
            </h3>
            <div>
                <input type="file" onChange={this.onFileChange} />
                <button onClick={this.onPostID}>
                  Post License!
                </button>
                <button onClick={this.onCheckID}>
                  Check License!
                </button>
            </div>
          {this.fileData()}
          {selectedResponse}
        </div>
      );
    }
  }
 
  export default App;
