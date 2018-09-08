import pytest
import os
import sys
import re
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
os.environ['SENTINEL_ENV'] = 'test'
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '../../lib')))
import config
from germancc_config import GermanccConfig


@pytest.fixture
def germancc_conf(**kwargs):
    defaults = {
        'rpcuser': 'germanccrpc',
        'rpcpassword': 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk',
        'rpcport': 29241,
    }

    # merge kwargs into defaults
    for (key, value) in kwargs.items():
        defaults[key] = value

    conf = """# basic settings
testnet=1 # TESTNET
server=1
rpcuser={rpcuser}
rpcpassword={rpcpassword}
rpcallowip=127.0.0.1
rpcport={rpcport}
""".format(**defaults)

    return conf


def test_get_rpc_creds():
    germancc_config = germancc_conf()
    creds = GermanccConfig.get_rpc_creds(germancc_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'germanccrpc'
    assert creds.get('password') == 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk'
    assert creds.get('port') == 76761

    germancc_config = germancc_conf(rpcpassword='s00pers33kr1t', rpcport=76761)
    creds = GermanccConfig.get_rpc_creds(germancc_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'germanccrpc'
    assert creds.get('password') == 's00pers33kr1t'
    assert creds.get('port') == 76761

    no_port_specified = re.sub('\nrpcport=.*?\n', '\n', germancc_conf(), re.M)
    creds = GermanccConfig.get_rpc_creds(no_port_specified, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'germanccrpc'
    assert creds.get('password') == 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk'
    assert creds.get('port') == 76761


# ensure germancc network (mainnet, testnet) matches that specified in config
# requires running germanccd on whatever port specified...
#
# This is more of a germanccd/jsonrpc test than a config test...
