from lto.accounts.account_factory_ed25519 import AccountFactoryED25519
from lto.public_node import PublicNode
from lto.transactions.anchor import Anchor
from lto.transactions.association import Association
from lto.transactions.revoke_association import RevokeAssociation



node = PublicNode('https://testnet.lto.network')
account = AccountFactoryED25519('T').create_from_seed('aaaaaaaaaaaaaaa')
account2 = AccountFactoryED25519('T').create_from_seed('bbbbbbbbbbbbbbb')
print(node.balance(account.address)/100000000)
print(node.balance(account2.address)/100000000)
anchor = '7ab62201df228f2c92ec74c29c61889b9658f4eef6a9a4a51bd25f23c9fcf376'
transaction = Anchor(anchor)
transaction.sign_with(account2)
transaction.sponsor_with(account)
tx = transaction.broadcast_to(node)




