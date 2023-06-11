import React, { Component, Fragment } from "react"; //(7)
import Header from "./components/Header";
import Home from "./components/Home";

class App extends Component { //(6)
 render() {
 return (
 <Fragment>
 <Header />
 <Home />
 </Fragment>
 );
 }
}

export default App;
