import click
from flask.cli import with_appcontext
from flask import current_app
from .seeders.seeder import Seeder
from .seeders.slots_seeder import seed_slots as seeder_seed_slots
from .models import SlotModel

@click.command("seed-all")
@with_appcontext
def seed_all():
    seeder = Seeder()
    seeder.seed_all()

@click.command("seed-slots")
@with_appcontext
def seed_slots():
    seeder = Seeder()
    seeder.add_seeder('slots', seeder_seed_slots)
    seeder.seed('slots')

@click.command("delete-empty-slots")
@with_appcontext
def delete_empty_slots():
    SlotModel.delete_old_empty()

@click.command("seed-roles")
@with_appcontext
def seed_roles():
    seeder = Seeder()
    seeder.seed('roles')

@click.command("seed-admin")
@with_appcontext
def seed_admin():
    Seeder.seed_admin()

@click.command("seed-test-user")
@with_appcontext
def seed_test_user():
    Seeder.seed_test_user()
