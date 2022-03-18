import os
TG_TOKEN_TEST = ''
TG_TOKEN_PROD = ''

PATH_PROD = ''


def is_prod():
    if 'OS' in os.environ and os.environ['OS'] == 'Windows_NT':
        return False
    else:
        return True


def get_tg_token():
    return TG_TOKEN_PROD if is_prod() else TG_TOKEN_TEST


def get_start_path():
    return PATH_PROD if is_prod() else ''
