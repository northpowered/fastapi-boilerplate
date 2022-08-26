import os
import glob

def clear_migrations_files():
    """
    Find and remove all migration files
    """
    current_dir: str = os.getcwd()
    migrations: list = list()
    for dir in os.walk(current_dir,followlinks=False):
        directory = os.path.relpath(dir[0],current_dir)
        if not directory.startswith('.') and 'piccolo_migrations' in directory:
            current_migrations: list = glob.glob(r'*.py',root_dir=directory)
            for current_migration in current_migrations:
                if current_migration != '__init__.py':
                    migrations.append(f"{directory}/{current_migration}")
    for migration in migrations:
        if os.path.isfile(migration):
            os.remove(migration)