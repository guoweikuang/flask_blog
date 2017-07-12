# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from my_blog.extensions import bcrypt
from flask_login import AnonymousUserMixin

db = SQLAlchemy()

posts_tags = db.Table('posts_tags',
    db.Column('post_id', db.String(64), db.ForeignKey('posts.id')),
    db.Column("tag_id", db.String(64), db.ForeignKey('tags.id'))
)

users_roles = db.Table(
    'users_roles',
    db.Column('user_id', db.String(45), db.ForeignKey('users.id')),
    db.Column('role_id', db.String(45), db.ForeignKey('roles.id')))


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(64), primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(128))
    """
    backref：用于指定表之间的双向关系，如果在一对多的关系中建立双向的关系，
             这样的话在对方看来这就是一个多对一的关系;
    lazy:  指定 SQLAlchemy 加载关联对象的方式。
        lazy=subquery: 会在加载 Post 对象后，将与 Post 相关联的对象全部加载，
        这样就可以减少 Query 的动作，也就是减少了对 DB 的 I/O 操作。但可能会返回大量不被使用的数据，会影响效率。
        lazy=dynamic: 只有被使用时，对象才会被加载，并且返回式会进行过滤，
        如果现在或将来需要返回的数据量很大，建议使用这种方式。Post 就属于这种对象
    """
    posts = db.relationship(
        'Post',
        backref="users",
        lazy="dynamic"
    )
    #roles = db.relationship(
    #    'Role',
    #    secondary=users_roles,
    #    backref=db.backref('users', lazy='dynamic')
    #)

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = self.set_password(password)

    def __repr__(self):
        return 'User Model from {}'.format(self.username)
    
    def set_password(self, password):
        """加密密码"""
        return bcrypt.generate_password_hash(password)

    def check_password(self, password):
        """核对密码"""
        return bcrypt.check_password_hash(self.password, password)
    
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True
    
    def is_active(self):
        return True

    def is_annoymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        return False

    def get_id(self):
        return unicode(self.id)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.String(64), primary_key=True)
    title = db.Column(db.String(128))
    text = db.Column(db.Text())
    create_time = db.Column(db.DateTime())
    user_id = db.Column(db.String(64), db.ForeignKey('users.id'))
    comments = db.relationship(
        'Comment',
        backref="posts",
        lazy="dynamic")
    tags = db.relationship(
        'Tag',
        secondary=posts_tags,
        backref=db.backref('posts', lazy='dynamic'),
        lazy="dynamic"
    )

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Post Model {}>'.format(self.title)


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Tag Model {}>".format(self.name)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.String(64), primary_key=True)
    comment = db.Column(db.Text())
    post_id = db.Column(db.String(64), db.ForeignKey('posts.id'))
    create_time = db.Column(db.DateTime())
    name = db.Column(db.String(64))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Comment Model {}>'.format(self.name)


