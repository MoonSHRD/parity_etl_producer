import logging

from eth_rpc_api import ParityEthJsonRpc


def infura_config(binder):
    logging.basicConfig(level=logging.INFO)
    binder.bind_to_constructor(ParityEthJsonRpc,
                               lambda: ParityEthJsonRpc("mainnet.infura.io/1f55c0f454d8475784d7b73d3d6d3f6e",
                                                        tls=True))



def base_config(binder):
    logging.basicConfig(level=logging.INFO)
    binder.bind_to_constructor(ParityEthJsonRpc, lambda: ParityEthJsonRpc("status.moonshrd.io"))
