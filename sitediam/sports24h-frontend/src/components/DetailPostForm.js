import React from "react";
import { Button, Form, FormGroup, Table } from "reactstrap";

class DetailPostForm extends React.Component {
    state = { // (32)
        // ('pk', 'owner', 'title', 'forum', 'text', 'likes_count', 'created_at')
        pk: 0,
        owner: "",
        title: "",
        forum: "",
        text: "",
        created_at: "",
        likes_count: 0,
        comment_set: []
    };
    componentDidMount() { // (33)
        if (this.props.post) {
            const { pk, owner, title, forum, text, likes_count, created_at } = this.props.post;
            this.setState({ pk, owner, title, forum, text, likes_count, created_at });
        }
        if (this.props.comments) { // (34)
            const allComments = this.props.comments;
            const post = this.props.post;
            const comment_set = [];
            for (let i = 0; i < allComments.length; i++) {
                if (post.pk === allComments[i].post){
                    comment_set.push(allComments[i]);
                }
            }
            this.setState({ comment_set });
        }
    }

    closeModalPost = e => {
        e.preventDefault();
        this.props.toggle();
    };
    defaultIfEmpty = value => {
        return value === "" ? "" : value;
    };
    render() { // (35)
        return (
            <Form onSubmit={this.closeModalPost}>
                <FormGroup>
                    <b>Text:</b>
                    <p>{this.defaultIfEmpty(this.state.text)} </p>
                </FormGroup>
                <FormGroup>
                    <b>Creation date:</b> &nbsp;
                    <p>{this.defaultIfEmpty(this.state.created_at)}</p>
                </FormGroup>
                <FormGroup>
                    <b>Owner:</b> &nbsp;
                    <p>{this.defaultIfEmpty(this.state.owner.name)}</p>
                </FormGroup>
                <FormGroup>
                    <b>Likes count:</b> &nbsp;
                    <p>{this.defaultIfEmpty(this.state.likes_count)}</p>
                </FormGroup>
                <FormGroup>
                    <Table>
                        <thead>
                        <tr>
                            <th colSpan="6" align="left">Comment</th>
                            <th colSpan="6" align="right">Creation Date</th>
                            <th></th>
                        </tr>
                        </thead>
                        <tbody> {/* (36) */}
                        {
                            !this.state.comment_set ||
                            this.state.comment_set.length <= 0 ? (
                                <tr>
                                    <td colSpan="14" align="left">
                                        <i>There are no comments.</i>
                                    </td>
                                </tr>
                            ) : (
                                this.state.comment_set.map((comment) =>
                                    <tr>
                                        <td colSpan="6" align="left">
                                            {comment.text}
                                        </td>
                                        <td colSpan="6" align="right">
                                            {comment.created_at}
                                        </td>
                                    </tr>
                                ))
                        }
                        </tbody>
                    </Table>
                </FormGroup>
                <Button>Close</Button> {/* (37) */}
            </Form>
        );
    }
}
export default DetailPostForm;

