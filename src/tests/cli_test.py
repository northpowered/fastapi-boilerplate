from typer.testing import CliRunner
from main import app
from .shared import clear_migrations_files
from .payloads import (
    test_superuser_1,
    test_superuser_2,
    test_user_1,
    test_user_2
)

runner = CliRunner()


def test_cli_db_drop_all():
    result = runner.invoke(app, ["db", "drop", "all"], input="y\n")
    assert result.exit_code == 0


def test_cli_db_drop_all_again():
    result = runner.invoke(app, ["db", "drop", "all"], input="y\n")
    assert result.exit_code == 0
    assert "Ignore" in result.stdout
    assert "Ignored" in result.stdout


def test_cli_db_init_all():
    result = runner.invoke(app, ["db", "init", "all"])
    assert result.exit_code == 0
    assert "Create" in result.stdout
    assert "Created" in result.stdout


def test_cli_db_init_all_again():
    result = runner.invoke(app, ["db", "init", "all"])
    assert result.exit_code == 0
    assert "Ignore" in result.stdout
    assert "Ignored" in result.stdout
    test_cli_db_drop_all()  # Let`s drop db for a right migration tests


def test_cli_db_mg_create_all():
    test_cli_db_drop_all()  # Double check - Let`s drop db for a right mg tests
    clear_migrations_files()  # Delete all mg in */piccolo_migrations dirs
    result = runner.invoke(app, ["db", "mg", "create", "all"])
    assert result.exit_code == 0


def test_cli_db_mg_run_all():
    test_cli_db_drop_all()
    result = runner.invoke(app, ["db", "mg", "run", "all"])
    assert result.exit_code == 0


def test_cli_db_show_all():
    result = runner.invoke(app, ["db", "show", "all"])
    assert result.exit_code == 0
    assert "1" in result.stdout


def test_cli_db_show_accounting():
    result = runner.invoke(app, ["db", "show", "accounting"])
    assert result.exit_code == 0
    assert "1" in result.stdout


def test_cli_db_show_wrong_app():
    result = runner.invoke(app, ["db", "show", "non-existing-app"])
    assert result.exit_code == 0
    assert "1" not in result.stdout


def test_cli_aaa_create_superuser():
    result = runner.invoke(app, ["aaa", "create", "superuser"], input=test_superuser_1.to_cli_input())
    assert result.exit_code == 0
    assert f"Superuser {test_superuser_1.username} was created with id" in result.stdout
    result = runner.invoke(app, ["aaa", "create", "superuser"], input=test_superuser_2.to_cli_input())
    assert result.exit_code == 0
    assert f"Superuser {test_superuser_2.username} was created with id" in result.stdout


def test_cli_aaa_create_user():
    result = runner.invoke(app, ["aaa", "create", "user"], input=test_user_1.to_cli_input())
    assert result.exit_code == 0
    assert f"User {test_user_1.username} was created with id" in result.stdout
    result = runner.invoke(app, ["aaa", "create", "user"], input=test_user_2.to_cli_input())
    assert result.exit_code == 0
    assert f"User {test_user_2.username} was created with id" in result.stdout


def test_cli_aaa_create_secret_from_config():
    result = runner.invoke(app, ["aaa", "create", "secret"])
    assert result.exit_code == 0
    assert "Secret generation completed" in result.stdout
    assert "All checks successfully passed" in result.stdout
