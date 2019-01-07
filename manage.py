from flask_script import Manager,Shell
from app import db,models,create_app
from flask_migrate import Migrate,MigrateCommand
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app,db)
def make_shell_context():
    return dict(db=db,User=models.User,Role=models.Role,app=app)

manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)



if __name__=='__main__':
    manager.run()


