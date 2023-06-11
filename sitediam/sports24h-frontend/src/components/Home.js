import React, { Component } from "react";
import { Col, Container, Row } from "reactstrap";
import PostList from "./PostList";

import axios from "axios"; //(12)

import {API_URL_POSTS, API_URL_COMMENTS, API_URL_USERS, API_URL_OWNERS} from "../constants";

//(13)
class Home extends Component { //(14)
 state = { //(15)
  posts: [],
  comments: [],
 };

 componentDidMount() { //(16)
  this.resetState();
 }

 getPosts = () => {
  axios.get(API_URL_POSTS).then(res => this.setState({ posts:
   res.data })); //(17)
    axios.get(API_URL_COMMENTS).then(res => this.setState({ comments:
   res.data })); //(17)
 };

 resetState = () => { //(16)
  this.getPosts();
 };

 render() {
  return (
      <Container style={{ marginTop: "20px" }}>
       <Row>
        <Col>
         <PostList
             posts={this.state.posts}
             comments={this.state.comments}
             resetState={this.resetState}
         />
        </Col>
       </Row>
      </Container>
  );
 }
}

export default Home;