#!/usr/bin/env python

import os

from hsm.db.sqlalchemy import migrate_repo

from migrate.versioning.shell import main


if __name__ == '__main__':
    main(debug='False',
         repository=os.path.abspath(os.path.dirname(migrate_repo.__file__)))
