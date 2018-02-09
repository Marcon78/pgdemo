#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_script import Manager, Server
from flask_script.commands import Clean
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
from app.models import Role, Employee, User, Subshop, SubshopRelationship


app = create_app()
manager = Manager(app)

manager.add_command("server", Server(host="0.0.0.0", port=8080))
manager.add_command("db", MigrateCommand)
manager.add_command("clean", Clean())

@manager.shell
def make_shell_context():
    return dict(app=app, db=db,
                Role=Role, Employee=Employee, User=User,
                SubshopRelationship=SubshopRelationship, Subshop=Subshop)

if __name__ == "__main__":
    manager.run()
