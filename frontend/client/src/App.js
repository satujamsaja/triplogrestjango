/**
https://www.valentinog.com/blog/socket-react/#What_you_will_learn
**/
import React, { Component } from "react";
import socketIOClient from "socket.io-client";
class App extends Component {
  constructor() {
    super();
    this.state = {
      response: false,
      endpoint: "http://127.0.0.1:8001"
    };
  }
  componentDidMount() {
    const { endpoint } = this.state;
    const socket = socketIOClient(endpoint);
    socket.on("FromAPI", data => this.setState({ response: data }));
  }
  render() {
    const { response } = this.state;
    console.log(response)
    return (
        <div style={{ textAlign: "center" }}>
          {response
              ? <TripList items={response} />
              : <p>Loading...</p>}
        </div>
    );
  }
}


class TripList extends React.Component {
  render() {
    return (
      <section>
        {this.props.items.map(item => (
          <div key={item.id}>
          <div>
          <p>{item.trip_name}<br/><span>{item.trip_date}</span><br/>{item.trip_body}</p>
          <LocationList items={item.trip_location} />
          </div>
          </div>
        ))}
      </section>
    );
  }
}


class LocationList extends React.Component {
  render() {
    return (
        <div>
            {this.props.items.map(item => (
              <p key={item.id}>{item.location_name}<br/><span>{item.location_date}</span><br/>{item.location_body}</p>
            ))}
        </div>
    );
  }
}

export default App;