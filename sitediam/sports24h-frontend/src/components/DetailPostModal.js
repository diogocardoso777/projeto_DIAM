import React, { Component, Fragment } from "react";
import { Button, Modal, ModalHeader, ModalBody } from "reactstrap";
import DetailPostForm from "./DetailPostForm";
class DetailPostModal extends Component {
  state = {
    modal: false // (25)
  };

  toggle = () => { // (26)
    this.setState(previous => ({
      modal: !previous.modal
    }));
  };


  render() {
    var title = "Post detail";
    var button = <Button onClick={this.toggle}
                         color="warning">Detail</Button>; // (27)
    return (
        <Fragment>
          {button} {/*(28)*/}
          <Modal isOpen={this.state.modal} toggle={this.toggle}>
            {/*(29)*/}
            <ModalHeader toggle={this.toggle}>{title}</ModalHeader>
            {/*(30)*/}
            <ModalBody> {/* (31) */}
              <DetailPostForm
                  resetState={this.props.resetState}
                  toggle={this.toggle}
                  post={this.props.post}
                  comments={this.props.comments}
              />
            </ModalBody>
          </Modal>
        </Fragment>
    );
  }
}

export default DetailPostModal;