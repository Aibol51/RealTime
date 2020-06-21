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

    admin = Admin()
    admin.name = 'admin'; admin.password = ae.encrypt('a');
    db.session.add(admin); db.session.commit();

if __name__ == '__main__':
    manager.run()
    # 启动方法: python manage.py runserver --port 5001