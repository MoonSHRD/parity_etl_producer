import argparse
import getopt
import json
import logging
import traceback
import sys

import inject

from block_inspector import BlockInspector
from conf import base_config
from extractors.EtherTransferExtractor import EtherTransferExtractor
from extractors.TokenTransferExtractor import TokenTransferExtractor
from mappers.transaction_mapper import TransactionMapper
from models.transaction import Transaction
from cent import Client

logger = logging.getLogger()


def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


def import_block(block):
    txs = []
    for tx_dict in block['transactions']:
        try:
            tx = TransactionMapper.json_dict_to_transaction(tx_dict)
            logger.info("Importing ", extra=tx_dict)
            for transfer in get_tx_value_transfers(tx):
                tx.add_transfer(transfer)
                txs.append(tx)


        except BaseException as e:
            logger.error(e, exc_info=True, extra=tx_dict)

    return txs


def get_tx_value_transfers(transaction: Transaction):
    transfers = []
    try:
        if transaction.block_number is None:
            return []

        for transfer in TokenTransferExtractor.extract(transaction):
            transfers.append(transfer)

        for transfer in EtherTransferExtractor.extract(transaction):
            transfers.append(transfer)

    except BaseException as e:
        logger.error(e, {"trace": traceback.format_exc(), "txid": transaction.hash})

    return transfers


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-c', default="./config.json", help='path to centrifugo config')
    parser.add_argument('-p', default="8000", help='centrifugo port')

    args = parser.parse_args()
    print(args)


    # centrifugo
    url = "http://localhost:"+args.__dict__['p']
    json_data = open(args.__dict__['c']).read()
    data = json.loads(json_data)
    api_key = data['api_key']
    client = Client(url, api_key=api_key, timeout=5)

    inject.configure(base_config)

    inspector = BlockInspector()

    while True:
        block = inspector.get_next_block()

        txs = import_block(block)

        for txsData in txs:
            print(txs)
            for key in txsData.totals:
                u_channel="totals#"+key
                c_clients = client.presence(u_channel)
                print(txsData.totals)
                if len(c_clients)>0:
                    for key1 in txsData.totals[key]:
                        data=txsData.totals[key][key1]
                        print(u_channel)
                        client.publish(u_channel, data)
