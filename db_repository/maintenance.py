from __future__ import unicode_literals
import multiprocessing

from migrate.versioning.api import version_control as create_db_version_control
from migrate.versioning.api import upgrade as upgrade_db_to_latest_schema
from migrate.versioning.api import downgrade as db_downgrade
from sqlalchemy import create_engine
from sqlalchemy.engine import reflection
from sqlalchemy.schema import DropTable
from sqlalchemy.schema import DropConstraint
from sqlalchemy.schema import ForeignKeyConstraint
from sqlalchemy.schema import MetaData
from sqlalchemy.schema import Table


def _downgrade_db(engine_uri, migration_repo):
    """We use multiprocessing here because the declarative base
    is set at a module level and all the classes registered to it
    end up declared again, which throws an error.

    """
    process = multiprocessing.Process(
        target=db_downgrade,
        args=(engine_uri, migration_repo,),
        kwargs={'version': 0},
    )
    process.start()
    process.join()


def _reflect_and_drop_all_tables(engine_uri):
    # Stolen from Michael Bayer
    # http://www.sqlalchemy.org/trac/wiki/UsageRecipes/DropEverything
    engine = create_engine(engine_uri)
    conn = engine.connect()

    # the transaction only applies if the DB supports
    # transactional DDL, i.e. Postgresql, MS SQL Server
    trans = conn.begin()

    inspector = reflection.Inspector.from_engine(engine)

    # gather all data first before dropping anything.
    # some DBs lock after things have been dropped in
    # a transaction.

    metadata = MetaData()

    tbs = []
    all_fks = []

    for table_name in inspector.get_table_names():
        fks = []
        for fk in inspector.get_foreign_keys(table_name):
            if not fk['name']:
                continue
            fks.append(ForeignKeyConstraint((), (), name=fk['name']))

        t = Table(table_name, metadata, *fks)
        tbs.append(t)
        all_fks.extend(fks)

    for fkc in all_fks:
        conn.execute(DropConstraint(fkc))

    for table in tbs:
        conn.execute(DropTable(table))

    trans.commit()


def db_init(engine_uri, migration_repo):
    # we have to downgrade the db because sometimes we might
    # have created Enum types that we need to destroy before we
    # re-create the database, otherwise we get an error telling
    # us that this type already exists.
    _downgrade_db(engine_uri, migration_repo)

    _reflect_and_drop_all_tables(engine_uri)

    create_db_version_control(engine_uri, migration_repo)

    upgrade_db_to_latest_schema(engine_uri, migration_repo)
