import logging
import traceback

import inject
from py._log.log import Producer

from block_inspector import BlockInspector
from conf import base_config
from extractors.EtherTransferExtractor import EtherTransferExtractor
from extractors.TokenTransferExtractor import TokenTransferExtractor
from mappers.transaction_mapper import TransactionMapper
from models.transaction import Transaction

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
    inject.configure(base_config)

    inspector = BlockInspector()
    producer = inject.attr(Producer)

    while True:
        block = inspector.get_next_block()

        txs = import_block()

        for data in txs:
            producer.poll(0)
            producer.produce('transactions', TransactionMapper.transaction_to_dict(data), callback=delivery_report)
            producer.flush()
