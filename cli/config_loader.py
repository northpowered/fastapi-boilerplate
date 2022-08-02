def set_config(config_file: str = 'config.ini')->None:
    import os
    os.environ['X_FA_CONF_FILE'] = config_file