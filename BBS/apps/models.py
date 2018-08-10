#!usr/bin/env python
#-*- coding:utf-8 -*- 

""" 
@author:yzk13 
@time: 2018/08/08 
"""
from exts import db
from datetime import datetime

class BannerModel(db.Model):
    __tablename__ = 'banner'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(255), nullable=False)
    link_url = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class BoardModel(db.Model):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class PostModel(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.String(100), db.ForeignKey("front_user.id"), nullable=False)

    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'))
    board = db.relationship("BoardModel", backref="posts")
    author = db.relationship("FrontUser", backref='posts')


class HighlightPostModel(db.Model):
    __tablename__ = 'hl_posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)

    post = db.relationship("PostModel", backref='highlight')


class CommentModel(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    author_id = db.Column(db.String(100), db.ForeignKey("front_user.id"), nullable=False)

    post = db.relationship('PostModel', backref='comments')
    author = db.relationship('FrontUser', backref='comments')