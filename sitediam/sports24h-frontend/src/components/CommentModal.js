import React, { Component, Fragment } from "react";
import { Button, Modal, ModalHeader, ModalBody } from "reactstrap";
import CommentForm from "./CommentForm";

class CommentModal extends Component {
    state = {
        modal: false
    };
    toggle = () => {
        this.setState(previous => ({
            modal: !previous.modal
        }));
    };
    render() {
        var title = "Comment";
        var button = <Button onClick={this.toggle}
                             color="danger">Comment</Button>;
        return (
            <Fragment>
                {button}
                <Modal isOpen={this.state.modal} toggle={this.toggle}>
                    <ModalHeader toggle={this.toggle}>{title}</ModalHeader>
                    <ModalBody>
                        <CommentForm
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

export default CommentModal;