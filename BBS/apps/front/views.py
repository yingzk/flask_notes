#!usr/bin/env python  
# -*- coding:utf-8 -*-

""" 
@author:yzk13 
@time: 2018/07/29 
"""

from flask import Blueprint, views, render_template, request, session, url_for, redirect, g, abort
from exts import db
from .forms import SignupForm, SigninForm, AddPostForm, AddCommentForm
from utils import restful, safeutils
from .models import FrontUser
from config import FRONT_USER_ID, PER_PAGE
from apps.models import BannerModel, BoardModel, PostModel, CommentModel, HighlightPostModel
from .decorators import login_required
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy.sql import func

bp = Blueprint('front', __name__)


@bp.route('/')
def index():
    # 分板块显示
    board_id = request.args.get('bd', type=int, default=None)
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    boards = BoardModel.query.all()
    # 分页
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    posts = None
    total = 0

    # 排序
    sort = request.args.get('st', type=int, default=None)
    query_obj = None
    if sort == 2:
        # 按照加精的时间进行排序
        query_obj = db.session.query(PostModel).outerjoin(HighlightPostModel).order_by(
            HighlightPostModel.create_time.desc(), PostModel.create_time.desc())
    elif sort == 3:
        """按照点赞排序"""
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 4:
        """按照评论数排序"""
        query_obj = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(
            func.count(CommentModel.id).desc(), PostModel.create_time.desc())
    else:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())

    if board_id:
        query_obj = query_obj.filter(PostModel.board_id==board_id)
        posts = query_obj.slice(start, end)
        total = query_obj.count()
    else:
        posts = query_obj.slice(start, end)
        total = query_obj.count()
    # bs_version: Bootstrap 版本
    # out_window: 分页条两端显示的页面数
    # inner_window: 分页条内显示页面数
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=1)
    context = {
        'banners': banners,
        'boards': boards,
        'posts': posts,
        'pagination': pagination,
        'current_board': board_id,
        'current_sort' : sort
    }
    return render_template('front/front_index.html', **context)


@bp.route('/p/<post_id>/')
def post_detail(post_id):
    """帖子详情页面"""
    post = PostModel.query.get(post_id)
    if post:
        return render_template('front/front_pdetail.html', post=post)
    else:
        abort(404)


@bp.route('/add_comment/', methods=['POST'])
@login_required
def add_comment():
    """添加评论"""
    form = AddCommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        post = PostModel.query.get(post_id)
        if post:
            comment = CommentModel(content=content)
            comment.post = post
            comment.author = g.front_user
            db.session.add(comment)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error('帖子不存在！')
    else:
        return restful.params_error(form.get_error())


@bp.route('/add_post/', methods=['GET', 'POST'])
@login_required
def add_post():
    """添加帖子"""
    if request.method == 'GET':
        boards = BoardModel.query.all()
        context = {
            'boards': boards
        }
        return render_template('front/front_addpost.html', **context)
    else:
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = BoardModel.query.get(board_id)
            if not board:
                return restful.params_error(message='没有这个板块！')
            post = PostModel(title=title, content=content)
            post.board = board
            post.author = g.front_user
            db.session.add(post)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


# 注册
class SignupView(views.MethodView):
    def get(self):
        # 获取之前的页面， 登陆后回到之前页面
        return_to = request.referrer
        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
            return render_template('front/front_signup.html', return_to=return_to)
        else:
            return render_template('front/front_signup.html')

    def post(self):
        form = SignupForm(request.form)
        if form.validate():
            # 存储数据到数据库中
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data
            user = FrontUser(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())


# 登录
class SigninView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and \
                return_to != url_for('front.signup') and \
                safeutils.is_safe_url(return_to):
            return render_template('front/front_signin.html', return_to=return_to)
        else:
            return render_template('front/front_signin.html')

    def post(self):
        form = SigninForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data

            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                session[FRONT_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_error(message='手机号或密码错误！')
        else:
            return restful.params_error(message=form.get_error())


bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))
bp.add_url_rule('/signin/', view_func=SigninView.as_view('signin'))


@bp.route('/signout/')
@login_required
def signout():
    del session[FRONT_USER_ID]
    return redirect(url_for('front.signin'))
