import React from "react";
import { Button, Form, FormGroup, Table } from "reactstrap";
import axios from "axios";
import { API_URL_OPCOES } from "../constants";
class CommentForm extends React.Component {
    state = {
        pk: 0,
        owner: "",
        title: "",
        forum: "",
        text: "",
        created_at: "",
        likes_count: 0,
        comment_set: [],
        //selectedOption: 0 // (38)
    };
    componentDidMount() {
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
    onChange = e => {
        this.setState({ [e.target.name]: e.target.value });
    };
/*    commentAndCloseModal = e => { // (41)
        e.preventDefault();
        for(let i=0; i<this.props.comments.length; i++){
            if(this.props.comments[i].pk == this.state.selectedOption){
                axios.put(API_URL_OPCOES + this.props.opcoes[i].pk,{'pk':
                    this.props.opcoes[i].pk,
                    'questao':
                    this.props.opcoes[i].questao,
                    'opcao_texto':
                    this.props.opcoes[i].opcao_texto,
                    'votos':
                        this.props.opcoes[i].votos++} );
            }
        }
        this.props.toggle();
    };*/
    defaultIfEmpty = value => {
        return value === "" ? "" : value;
    };
    handleOptionChange = changeEvent => { // (40)
        const optionid = changeEvent.target.value;
        //this.state.selectedOption = optionid;
    };

    handleSubmit = (e) => {
        e.preventDefault();
        // Perform any necessary actions with the selected option
        console.log("Selected option:", this.state.selectedOption);
    };
    render() {
        return (
            <Form onSubmit={this.handleSubmit}>
                <FormGroup>
                    <b>Text:</b>
                    <p>{this.defaultIfEmpty(this.state.text)} </p>
                </FormGroup>
                <FormGroup>
                    <b>Created at:</b> &nbsp;
                    <p>{this.defaultIfEmpty(this.state.created_at)}</p>
                </FormGroup>
                <FormGroup>
                    <Table>
                        <thead>
                        <tr>
                            <th colSpan="6" align="left">Comment</th>
                        </tr>
                        </thead>
                        <tbody>
                        {
                            !this.state.comment_set ||
                            this.state.comment_set.length <= 0 ? (
                                <tr>
                                    <td colSpan="14" align="left">
                                        <i>No comments.</i>
                                    </td>
                                </tr>
                            ) : (
                                this.state.comment_set.map((comment) =>
                                    <tr>
                                        <td colSpan="6" align="left">
                                            &nbsp;&nbsp;
                                            <label>
                                                <input
                                                    type="radio"
                                                    name="react-radio"
                                                    value={comment.pk}
                                                    checked={false}
                                                    className="form-check-input"

                                                    onChange={this.handleOptionChange} // (39)
                                                />
                                                &nbsp;&nbsp;{comment.text}
                                            </label>
                                        </td>
                                    </tr>
                                ))
                        }
                        </tbody>
                    </Table>
                </FormGroup>
                <Button>Back</Button>
            </Form>
        );
    }
}
export default CommentForm;
