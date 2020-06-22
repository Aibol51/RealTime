# Flask 库 (核心库)
from flask import (Blueprint,
                   render_template, url_for, jsonify,
                   request)

# 自建库 (各种功能)
from App.models import *
from App.functions import *
from App.decoretors import *

# Python自带库 (辅助功能)
from datetime import datetime

home_blue = Blueprint('home_blue', __name__, template_folder='../templates', static_folder='../static')


def init_home_blue(app):
    app.register_blueprint(blueprint=home_blue)


@home_blue.route('/')
def index():
    return render_template('index.html')

@home_blue.route('/reg_log')
def reg_log():
    return render_template('reg_log.html')

@home_blue.route('/about')
def about():
    return render_template('about.html')

@home_blue.route('/detail/<item_id>')
def detail(item_id):
    return render_template('detail.html')

# 申请购买(详情页面内)
@home_blue.route('/seed_request', methods=['POST'])
def seed_request():
    contact = request.form.get('contact')
    total = request.form.get('total')
    result = 0

    if contact and total.isdigit():
        result = 1
    else:
        result = 0

    return jsonify({'result': result})

@home_blue.route('/log', methods=['POST'])
def log():
    name = request.form.get('name')
    pwd = request.form.get('pwd')
    result = 0

    if name and pwd:
        admin = Admin.query.filter(Admin.name == name).first()
        if admin:
            aes_encrypt = AES_ENCRYPT()
            if aes_encrypt.decrypt(admin.password).decode() == pwd:
                session['admin_login'] = admin.id
                session.permanent = True  # 浏览器关闭也不会影响登陆状态, 默认31天;
                # return redirect(url_for('home_blue.admin'))
                result = 1
            else: # 密码错误
                result = 0
        else: # 账户不存在
            result = -1
    else: # 输入的数据不完整
        result = 2

    return jsonify({'result': result})


#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#           ↓ Admin 页面 ↓            #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

@home_blue.route('/admin_logout')
@adminLogRequired
def admin_logout():
    admin = Admin.query.filter(Admin.id == session.get('admin_login')).first()
    admin.login_time = str(datetime.now())[:str(datetime.now()).rfind('.'):]
    db.session.commit(); session.pop('admin_login');

    return redirect(url_for('home_blue.index'))

@home_blue.route('/admin')
@adminLogRequired
def admin():
    admin = Admin.query.filter(Admin.id == session.get('admin_login')).first()
    return render_template('admin/index.html', admin=admin)