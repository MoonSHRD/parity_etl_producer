import logging

from eth_rpc_api import ParityEthJsonRpc


def base_config(binder):
    logging.basicConfig(level=logging.INFO)
    binder.bind_to_constructor(ParityEthJsonRpc, lambda: ParityEthJsonRpc("status.moonshrd.io"))
