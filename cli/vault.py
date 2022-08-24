import typer
import asyncio
from .config_loader import set_config, config_default
from .console import info,warning,success,error
from configuration import config
from utils import vault

app = typer.Typer(
    no_args_is_help=True,
    short_help='Hashicorp Vault management'
)

@app.command(short_help='Check Vault state')
def check(c: str = config_default):
    """
    Check Vault instance status
    """
    set_config(c)
    vault.load_auth_data()
    status: bool = asyncio.run(vault.check_vault_state())
    if status:
        success('Vault instance is ready')
    else:
        warning('Vault instance is unavailable')



@app.command(short_help='Creating objects', no_args_is_help=True)
def init(c: str = config_default):
    """
    Init Vault secrets storage
    """
    set_config(c)
    vault.load_auth_data()
    vault.get_instance()