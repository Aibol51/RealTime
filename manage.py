from flask_script import Manager
from flask_migrate import MigrateCommand
from App import create_app

from App.functions import *

app = create_app()

manager = Manager(app=app)
manager.add_command('db', MigrateCommand)

@manager.command
def seed():
    '''
    :return: 将初始数据加载到数据库中 / Load initial data into database
    '''
    ae = AES_ENCRYPT()

    admin, dev = Admin(), Admin()
    admin.name = 'orken'; admin.password = ae.encrypt('abc123'); admin.superuser = 1;
    dev.name = 'dev'; dev.password = ae.encrypt('false'); dev.superuser = 1;
    db.session.add(admin); db.session.commit();

    about = About()
    about.company_name = '公司名称'
    about.img1 = 'img/company_picture1.jpg'; about.img2 = 'img/company_picture2.jpg'; about.img3 = 'img/company_picture3.jpg';
    about.content = '''公司的描述...公司的描述...公司的描述...公司的描述...公司的描述...公司的描述...
        公司的描述...公司的描述...公司的描述...公司的描述...公司的描述...公司的描述...公司的描述...公司的描述...公司的描述...
        公司的描述...公司的描述...公司的描述...公司的描述...公司的描述...公司的描述...公司的描述...公司的描述...公司的描述...
        公司的描述...公司的描述...公司的描述...公司的描述...公司的描述...公司的描述...公司的描述...公司的描述...公司的描述...
        公司的描述...公司的描述...公司的描述...公司的描述...公司的描述...公司的描述...公司的描述...公司的描述...公司的描述...'''

    db.session.add(about); db.session.commit();

    # 统计网站浏览量
    visit = Visit()
    visit.visit_num = 0;
    db.session.add(visit); db.session.commit();

if __name__ == '__main__':
    manager.run()
    # 启动方法: python manage.py runserver --port 5000
