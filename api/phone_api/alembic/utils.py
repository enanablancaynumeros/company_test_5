from os import path

from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory

from api.phone_api.db_connection import create_db_if_not_exists

alembic_cfg = Config()
scripts_folder = path.dirname((path.abspath(__file__)))
alembic_cfg.set_main_option("script_location", scripts_folder)
script = ScriptDirectory.from_config(alembic_cfg)


def alembic_autogenerate():
    command.revision(alembic_cfg, autogenerate=True, rev_id="0", message="")


def alembic_downgrade_base():
    command.downgrade(alembic_cfg, revision="base")


def alembic_upgrade_head():
    command.upgrade(alembic_cfg, revision="head")


def recreate_postgres_metadata():
    create_db_if_not_exists()
    alembic_downgrade_base()
    alembic_upgrade_head()
