import click
from werkzeug.security import generate_password_hash
from polls.models import User
from admin.routes import admin_blueprint
from app_factory import db


admin_blueprint.cli.help = 'Perform admin commands.'


@admin_blueprint.cli.command('createsuperuser', help='Create an admin user.')
@click.argument('username')
@click.password_option()
def register_superuser(username, password):
    password_hash = generate_password_hash(password, method='scrypt:32768:8:1')

    if User.query.filter(User.username == username).first():
        click.echo('The username is already taken.')
        return False

    user = User(username=username,
                password=password_hash,
                is_superuser=True)
    db.session.add(user)
    db.session.commit()

    click.echo('The superuser has been successfully created.')
