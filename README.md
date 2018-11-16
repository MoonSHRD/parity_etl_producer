Так выглядит обработанная транзакция перед загрузкой в Consumer  (см пояснекния)

```json5

{'block_hash': '0xc9eea38a08e7a73773231caa945217740fd879e5c0bf447881dc82b3f0bfadd2',
 'block_number': 6712643,
 'from_address': '0xb8fa4a1f74bc05b4a21ebb52313fc41da1853922',
 'gas': 250000,
 'gas_price': 17000000000,
 'hash': '0x566ab3d39cce49d18c6767e1c47bbd81f8b3a86730d286781db6c72270a46dac',
 'input': '0x338b5dea00000000000000000000000023ccc43365d9dd3882eab88f43d515208f83243000000000000000000000000000000000000000000000033d6a27492034900000',
 'nonce': 1,
 'to_address': '0x2a0c0dbecc7e4d658f48e01e3fa353f44050c208',
//Total - Отражает передлачу определенного ассета  - ключ либо адрес токена либо 0 для эфира - данные аггрегируется (важно колгда много внутренних вызовов) 
 'totals': {'0x2a0c0dbecc7e4d658f48e01e3fa353f44050c208': {'0x23ccc43365d9dd3882eab88f43d515208f832430': {'from': '0xb8fa4a1f74bc05b4a21ebb52313fc41da1853922',
                                                                                                          'received': 15300000000000000000000,
                                                                                                          'sent': 0,
                                                                                                          'to': None}},
            '0xb8fa4a1f74bc05b4a21ebb52313fc41da1853922': {'0x23ccc43365d9dd3882eab88f43d515208f832430': {'from': None,
                                                                                                          'received': 0,
                                                                                                          'sent': 15300000000000000000000,
                                                                                                          'to': '0x2a0c0dbecc7e4d658f48e01e3fa353f44050c208'}}},
 'transaction_index': 2,
// Здесь отражен каждый трансфер ценности 
 'transfers': [{'block_number': 6712643,
                'from_address': '0xb8fa4a1f74bc05b4a21ebb52313fc41da1853922',
                'to_address': '0x2a0c0dbecc7e4d658f48e01e3fa353f44050c208',
                'transaction_hash': '0x566ab3d39cce49d18c6767e1c47bbd81f8b3a86730d286781db6c72270a46dac',
                'value': 15300000000000000000000,
                'value_id': '0x23ccc43365d9dd3882eab88f43d515208f832430'}],
 'type': 'transaction',
 'value': 0}
 ```
 
 
 
