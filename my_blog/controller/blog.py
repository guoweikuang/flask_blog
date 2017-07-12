# -*- coding: utf-8 -*-
from datetime import datetime
import os

from uuid import uuid4
from flask import render_template, Blueprint, redirect, url_for
from sqlalchemy import func

# from main import app
from my_blog.models import db, Post, User, Comment, Tag, posts_tags
from my_blog.forms import CommentForm, PostForm

print(os.path.join(os.path.pardir, 'templates', 'my_blog')) 
blog_buleprint = Blueprint(
    'my_blog',
    __name__,
    template_folder=os.path.join(os.path.pardir, 'templates', 'my_blog'),
    url_prefix='/blog')


def sidebar_data():
    """ 右侧边栏视图 """
    recent = db.session.query(Post).order_by(
        Post.create_time.desc()
    ).limit(5).all()
    top_tags = db.session.query(
        Tag, func.count(posts_tags.c.post_id).label('total')
        ).join(posts_tags).group_by(Tag).order_by('total DESC').limit(5).all()
    return recent, top_tags


@blog_buleprint.route('/')
@blog_buleprint.route('/<int:page>')
def home(page=1):
    """主页"""
    posts = Post.query.order_by(
        Post.create_time.desc()
    ).paginate(page, 10)

    recent, top_tags = sidebar_data()

    return render_template('home.html',
                           posts=posts,
                           recent=recent,
                           top_tags=top_tags)


@blog_buleprint.route('/post/<string:post_id>', methods=('GET', 'POST'))
def post(post_id):
    """文章视图"""
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(name=form.name.data)
        new_comment.id = str(uuid4())
        new_comment.comment = form.text.data
        new_comment.create_time = datetime.now()
        new_comment.post_id = post_id
        db.session.add(new_comment)
        db.session.commit()
    post = Post.query.get_or_404(post_id)
    # post = db.session.query(Post).get_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.create_time.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template('post.html',
                           post=post,
                           tags=tags,
                           form=form,
                           comments=comments,
                           recent=recent,
                           top_tags=top_tags)


@blog_buleprint.route('/tag/<string:tag_name>')
def tag(tag_name):
    """标签页视图"""
    tag = db.session.query(Tag).filter_by(name=tag_name).first_or_404()
    posts = tag.posts.order_by(Post.create_time.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template('tag.html',
                           tag=tag,
                           posts=posts,
                           recent=recent,
                           top_tags=top_tags)


@blog_buleprint.route('/user/<string:username>')
def username(username):
    """用户视图"""
    user = db.session.query(User).filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.create_time.desc()).all
    recent, top_tags = sidebar_data()

    return render_template('user.html',
                           user=user,
                           posts=posts,
                           recent=recent,
                           top_tags=top_tags)


@blog_buleprint.route('/new', methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data)
        new_post.id = str(uuid4())
        new_post.create_time = datetime.now()
        new_post.text = form.text.data

        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('my_blog.home'))
    return render_template('new_post.html', form=form)


@blog_buleprint.route('/edit_post/<string:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        post.create_time = datetime.now()

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('my_blog.post', post_id=post.id))
    form.title.data = post.title
    form.text.data = post.text
    return render_template('edit_post.html', form=form, post=post)



    

