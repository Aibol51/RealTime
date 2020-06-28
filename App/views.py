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
from os import remove as os_remove
from random import randint, choice

home_blue = Blueprint('home_blue', __name__, template_folder='../templates', static_folder='../static')


def init_home_blue(app):
    app.register_blueprint(blueprint=home_blue)

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#           ↓ User 页面 ↓             #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

@home_blue.route('/')
def index():
    # for i in range(30):
    #     item = Item()
    #     item.name = 'test'+str(i)
    #     item.price = randint(100, 5000)
    #     item.total = randint(1, 600)
    #     db.session.add(item); db.session.commit()


    items = Item.query.filter(Item.total >= 1).all()
    calc_view() # 计算网页浏览量
    return render_template('index.html', items=items)

@home_blue.route('/search', methods=['POST'])
def search():
    search_text = request.form.get('search_text')
    result = 'fail'

    if search_text:
        result = []
        result.extend(Item.query.filter(Item.name == search_text).all())
        result.extend(Item.query.filter(Item.detail_info.contains(search_text)).all())

        print(result)

    return jsonify({'result': result})

@home_blue.route('/reg_log')
def reg_log():
    calc_view()  # 计算网页浏览量
    return render_template('reg_log.html')

@home_blue.route('/about')
def about():
    company = About.query.all()[0]
    calc_view()  # 计算网页浏览量
    return render_template('about.html', company=company)

@home_blue.route('/detail/<item_id>')
def detail(item_id):
    item = Item.query.filter(Item.id == item_id).first()
    calc_view()  # 计算网页浏览量
    item.view_num += 1
    db.session.commit()
    return render_template('detail.html', item=item)

# 申请购买(详情页面内)
@home_blue.route('/seed_request', methods=['POST'])
def seed_request():
    contact = request.form.get('contact')
    total = request.form.get('total')
    item_id = request.form.get('item_id')
    result = 0

    if contact and total.isdigit():
        req = Request()
        req.contact = contact
        req.total = int(total)
        req.objective_item = int(item_id)

        db.session.add(req); db.session.commit();

        item = Item.query.filter(Item.id == item_id).first()
        item.total -= 1

        db.session.commit()

        result = 1
    else:
        result = 0

    return jsonify({'result': result})

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#            ↓ 公共区域 ↓              #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

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

@logRequired
@home_blue.route('/change_name', methods=['POST'])
def change_name():
    admin = Admin.query.filter(Admin.name == request.form.get('old_name')).first()
    result = 0

    if request.form.get('old_name'):
        if detection('name', request.form.get('new_name')):
            admin.name = request.form.get('new_name')
            db.session.commit()
            result = 1
        else:
            # 无效用户名(不符合命名规范)
            result = 0
    else: # 无效用户名(为空)
        result = 0

    return jsonify({'result': result})

@logRequired
@home_blue.route('/change_pwd', methods=['POST'])
def change_pwd():
    admin = Admin.query.filter(Admin.name == request.form.get('name')).first()
    result = 0

    if request.form.get('old_pwd') and request.form.get('new_pwd'):
        aes_encrypt = AES_ENCRYPT()
        if aes_encrypt.decrypt(admin.password).decode() == request.form.get('old_pwd'):
            if detection('pwd', request.form.get('old_pwd')):
                admin.password = aes_encrypt.encrypt(request.form.get('new_pwd'))
                db.session.commit()
                result = 1
            else: # 不符合密码规范
                result = 2
        else: # 旧密码不正确
            result = 0
    else: # 没有输入
        result = -1

    return jsonify({'result': result})

@logRequired
@home_blue.route('/upload_photo', methods=['POST'])
def upload_photo():
    result = 0
    if 'img1' in request.files:
        photo = request.files.get('img1')

        if photo:
            if allowed_file(photo.filename):
                company = About.query.all()[0]
                os_remove('App/static/'+company.img1)

                photo.save('App/static/img/company_picture1' + photo.filename[photo.filename.rfind('.'):])

                company.img1 = 'img/company_picture1'+photo.filename[photo.filename.rfind('.'):]
                db.session.commit()
                result = 1
            else: # 不支持文件类型
                result = -1
    elif 'img2' in request.files:
        photo = request.files.get('img2')

        if photo:
            if allowed_file(photo.filename):
                company = About.query.all()[0]
                os_remove('App/static/' + company.img2)
                photo.save('App/static/img/company_picture2'+photo.filename[photo.filename.rfind('.'):])
                company.img1 = 'img/company_picture2'+photo.filename[photo.filename.rfind('.'):]
                db.session.commit()
                result = 1
            else: # 不支持文件类型
                result = -1
    elif 'img3' in request.files:
        photo = request.files.get('img3')

        if photo:
            if allowed_file(photo.filename):
                company = About.query.all()[0]
                os_remove('App/static/' + company.img3)
                photo.save('App/static/img/company_picture3'+photo.filename[photo.filename.rfind('.'):])
                company.img1 = 'img/company_picture3'+photo.filename[photo.filename.rfind('.'):]
                db.session.commit()
                result = 1
            else: # 不支持文件类型
                result = -1

    return jsonify({'result': result})

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#           ↓ Admin 页面 ↓            #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

@adminLogRequired
@home_blue.route('/admin_logout')
def admin_logout():
    admin = Admin.query.filter(Admin.id == session.get('admin_login')).first()
    admin.login_time = str(datetime.now())[:str(datetime.now()).rfind('.'):]
    db.session.commit(); session.pop('admin_login');

    return redirect(url_for('home_blue.index'))

@adminLogRequired
@home_blue.route('/admin')
def admin():
    admin = Admin.query.filter(Admin.id == session.get('admin_login')).first()
    request_num = Request.query.count()
    calc_view()  # 计算网页浏览量
    return render_template('admin/index.html', admin=admin, request_num=request_num)

@adminLogRequired
@home_blue.route('/admin_profile')
def admin_profile():
    admin = Admin.query.filter(Admin.id == session.get('admin_login')).first()
    request_num = Request.query.count()
    calc_view()  # 计算网页浏览量
    return render_template('admin/profile.html', admin=admin, request_num=request_num)

@adminLogRequired
@home_blue.route('/admin_about')
def admin_about():
    admin = Admin.query.filter(Admin.id == session.get('admin_login')).first()
    request_num = Request.query.count()
    company = About.query.all()[0]
    calc_view()  # 计算网页浏览量
    return render_template('admin/about.html', admin=admin, company=company, request_num=request_num)

@adminLogRequired
@home_blue.route('/change_company_name', methods=['POST'])
def change_company_name():
    new_name = request.form.get('new_company_name')
    result = 0

    if new_name:
        company = About.query.all()[0]
        company.company_name = new_name
        db.session.commit()
        result = 1

    return jsonify({'result': result})

@adminLogRequired
@home_blue.route('/change_company_content', methods=['POST'])
def change_company_content():
    new_content = request.form.get('new_company_content')
    result = 0

    if new_content:
        company = About.query.all()[0]
        company.content = new_content
        db.session.commit()
        result = 1

    return jsonify({'result': result})

@adminLogRequired
@home_blue.route('/item', methods=['GET', 'POST'])
def item():
    admin = Admin.query.filter(Admin.id == session.get('admin_login')).first()
    request_num = Request.query.count()
    items = Item.query.all()
    calc_view()  # 计算网页浏览量

    if request.method == 'GET':
        return render_template('admin/item.html', admin=admin, items=items, request_num=request_num)
    else: # POST
        name = request.form.get('add_item_name')
        price = request.form.get('add_item_price')
        total = request.form.get('add_item_total')
        img = request.files.get('add_item_img')
        detail_info = request.form.get('add_item_detail_info')

        if name and price and total and img and detail_info:
            item = Item()
            item.name = name
            item.price = price
            item.total = total
            r_num = str(randint(0, 99))
            now_time = str(datetime.now())[:str(datetime.now()).rfind('.'):]
            now_time = now_time.replace(':', ''); now_time = now_time.replace(' ', '');
            img.save('App/static/img/'+r_num+now_time+img.filename[img.filename.rfind('.'):])
            item.img = 'img/'+r_num+now_time+img.filename[img.filename.rfind('.'):]
            item.detail_info = detail_info

            db.session.add(item); db.session.commit()
            done_text2 = '添加成功!'
        else:
            done_text2 = '添加失败!'

        return render_template('admin/item.html', admin=admin, items=items, done_text2=done_text2, request_num=request_num)

@adminLogRequired
@home_blue.route('/del_item', methods=['POST'])
def del_item():
    item = Item.query.filter(Item.id == request.form.get('item_id')).first()
    os_remove('App/static/'+item.img)
    db.session.delete(item); db.session.commit();

    return jsonify({'result': 'ok'})

@adminLogRequired
@home_blue.route('/request_page')
def request_page():
    admin = Admin.query.filter(Admin.id == session.get('admin_login')).first()
    requests = Request.query.all()
    request_num = Request.query.count()
    items = []
    for i in requests:
        items.append(Item.query.filter(Item.id == i.objective_item).first())
    calc_view()  # 计算网页浏览量
    return render_template('admin/request_page.html', admin=admin, requests=requests, request_num=request_num, items=items)

@adminLogRequired
@home_blue.route('/del_req', methods=['POST'])
def del_req():
    req = Request.query.filter(Request.id == request.form.get('req_id')).first()
    db.session.delete(req); db.session.commit();

    return jsonify({'result': 'ok'})