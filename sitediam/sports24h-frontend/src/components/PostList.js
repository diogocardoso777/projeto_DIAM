import React, { Component } from "react";
import { Table } from "reactstrap";
import CommentModal from "./CommentModal";
import DetailPostModal from "./DetailPostModal";
//import DetailPostModal from "../test/DetailPostModal";


class PostList extends Component {
    render() {
        const posts = this.props.posts; {/* (20) */}
        const comments = this.props.comments;
        return (
            <Table light> {/* (21) */}
                <thead> {/* (22) */}
                <tr>
                    <th>Text</th>
                    <th>Creation date</th>
                    <th>Owner</th>
                    <th>Like count</th>
                    <th></th>
                </tr>
                </thead>
                <tbody> {/* (23) */}
                {!posts || posts.length <= 0 ? (
                    <tr>
                        <td colSpan="6" align="center">
                            <b>There are no posts.</b>
                        </td>
                    </tr>
                ) : (
                    posts.map(post => ( // (24)  # 'pk', 'owner', 'title', 'forum', 'text', 'likes_count', 'created_at'
                        <tr key={post.pk}>
                            <td>{post.text}</td>
                            <td>{post.created_at}</td>
                            <td>{post.owner.name}</td>
                            <td>{post.likes_count}</td>

                            <td align="center">
                               <DetailPostModal
                                    create={false}
                                    post={post}
                                    comments={comments}
                                    resetState={this.props.resetState}
                                />
                                &nbsp;&nbsp;
                               <CommentModal
                                    post={post}
                                    comments={comments}
                                    resetState={this.props.resetState}
                                />
                            </td>
                        </tr>
                    ))
                )}
                </tbody>
            </Table>
        );
    }
}

export default PostList;