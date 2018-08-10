#!usr/bin/env python  
# -*- coding:utf-8 -*-

""" 
@author:yzk13 
@time: 2018/07/29 
"""

from flask import Blueprint, render_template, views, request, session, g
from flask_mail import Message
import string, random
from exts import db, mail
from .models import CMSUser, CMSPermission
from .forms import *
from .decorators import *
from config import CMS_USER_ID
from utils import restful, ycache
from apps.models import BannerModel, BoardModel, PostModel, HighlightPostModel
import tasks

bp = Blueprint('cms', __name__, url_prefix='/cms')


@bp.route('/')
@login_required
def index():
    """首页"""
    return render_template('cms/cms_index.html')


@bp.route('/logout/')
@login_required
def logout():
    """注销"""
    # session.clear()
    del session[CMS_USER_ID]
    return redirect(url_for('cms.login'))


@bp.route('/profile/')
@login_required
def profile():
    """信息查看"""
    return render_template('cms/cms_profile.html')


@bp.route('/email_captcha/')
def email_captcha():
    email = request.args.get('email')
    if not email:
        return restful.params_error(message='请输入邮箱')
    # 生成验证码，并发送
    source = list(string.ascii_letters)
    # source.extend(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'])
    source.extend(map(lambda x: str(x), range(0, 10)))
    captcha = "".join(random.sample(source, 6))

    # message = Message('BBS验证码', recipients=[email], body='验证码为：%s' % captcha)
    # try:
    #     mail.send(message)
    # except:
    #     return restful.server_error()

    tasks.send_mail.delay('BBS验证码', [email], '验证码为：%s' % captcha)
    ycache.set(email, captcha)
    return restful.success()


@bp.route('/test_email/')
def send_email():
    message = Message('testing', recipients=['yzk.1314@outlook.com'], body='test')
    mail.send(message)
    return "发送成功"


@bp.route('/posts/')
@login_required
@permission_required(CMSPermission.POSTER)
def posts():
    """帖子管理"""
    context = {
        'posts': PostModel.query.all()
    }
    return render_template('cms/cms_posts.html', **context)


@bp.route('/highlight/', methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def highlight():
    """帖子加精"""
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error('请传入帖子ID！')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error('帖子不存在！')
    highlight = HighlightPostModel()
    highlight.post = post
    db.session.add(highlight)
    db.session.commit()
    return restful.success()


@bp.route('/d_highlight/', methods=['POST'])
def d_highlight():
    """取消加精"""
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error('请传入帖子ID！')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error('帖子不存在！')
    highlight = HighlightPostModel.query.filter_by(post_id=post_id).first()
    db.session.delete(highlight)
    db.session.commit()
    return restful.success()



@bp.route('/comments/')
@login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    """评论管理"""
    return render_template('cms/cms_comments.html')


@bp.route('/boards/')
@login_required
@permission_required(CMSPermission.BOARDER)
def boards():
    """板块管理"""
    board_models = BoardModel.query.order_by(BoardModel.create_time.desc()).all()
    context = {
        'boards':board_models
    }
    return render_template('cms/cms_boards.html', **context)

@bp.route('/add_board/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def add_board():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(form.get_error())

@bp.route('/edit_board/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def edit_board():
    form = EditBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.get(board_id)
        if board:
            board.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个板块！')
    else:
        return restful.params_error(message=form.get_error())

@bp.route('/delete_board/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def delete_board():
    board_id = request.form.get('board_id')
    if not board_id:
        return restful.params_error(message='请传入板块ID！')
    board = BoardModel.query.get(board_id)
    if not board:
        return restful.params_error('板块不存在！')
    db.session.delete(board)
    db.session.commit()
    return restful.success()

@bp.route('/fusers/')
@login_required
@permission_required(CMSPermission.FRONTUSER)
def fusers():
    return render_template('cms/cms_fusers.html')


@bp.route('/cusers/')
@login_required
@permission_required(CMSPermission.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html')


@bp.route('/croles/')
@login_required
@permission_required(CMSPermission.ADMINISTRATOR)
def croles():
    return render_template('cms/cms_croles.html')


@bp.route('/banners/')
@login_required
def banners():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template('cms/cms_banners.html', banners=banners)


@bp.route('/add_banner/', methods=['POST'])
@login_required
def add_banner():
    """添加轮播图"""
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data

        banner = BannerModel(name=name, image_url=image_url, link_url=link_url, priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/edit_banner/', methods=['POST'])
@login_required
def edit_banner():
    """编辑轮播图"""
    form = EditBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data

        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个轮播图！')
    else:
        return restful.params_error(message=form.get_error())

@bp.route('/delete_banner/', methods=['POST'])
@login_required
def delete_banner():
    """删除轮播图"""
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error(message='请传入轮播图ID！')

    banner = BannerModel.query.get(banner_id)
    if not banner:
        return restful.params_error(message='轮播图不存在！')

    db.session.delete(banner)
    db.session.commit()
    return restful.success()


# 登录
class LoginView(views.MethodView):
    def get(self, message=None):
        return render_template('cms/cms_login.html', message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[CMS_USER_ID] = user.id
                if remember:
                    # 设置过期时间为31天
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                return self.get(message='邮箱或密码错误')
        else:
            return self.get(message=form.errors)


# 修改密码
class ResetPwdView(views.MethodView):
    # 添加装饰器
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetPwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            # 判断密码是否正确
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                # 返回json数据给前端
                return restful.success()
            else:
                return restful.params_error(message='原始密码错误')
        else:
            message = form.get_error()
            return restful.params_error(message=message)


# 修改邮箱
class ResetEmailView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))
