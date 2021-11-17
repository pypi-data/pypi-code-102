from LTOCli import handle_default as handle
from LTO.Transactions.lease import Lease
from LTO.Transactions.cancel_lease import CancelLease


def func(name_space, parser):
    if vars(name_space)['subparser-name-lease']:
        chain_id = handle.check(name_space.network[0], parser) if name_space.network else 'L'
        account_name = vars(name_space)['account'][0] if vars(name_space)['account'] else ''
        sponsor = vars(name_space)['sponsor'][0] if vars(name_space)['sponsor'] else None

    if vars(name_space)['subparser-name-lease'] == 'create':
        transaction = Lease(recipient=name_space.recipient[0], amount=name_space.amount[0])
        if vars(name_space)['unsigned'] is False:
            transaction.sign_with(handle.get_account(chain_id, parser, account_name))
            if sponsor:
                transaction.sponsor_with(handle.get_account(chain_id, parser, sponsor))
            if vars(name_space)['no_broadcast'] is False:
                transaction = transaction.broadcast_to(handle.get_node(chain_id, parser))
        elif vars(name_space)['no_broadcast'] is False:
            parser.error(
                "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto lease create --help' for more informations ")
        handle.pretty_print(transaction)

    elif vars(name_space)['subparser-name-lease'] == 'cancel':
        transaction = CancelLease(leaseId=name_space.leaseId[0])
        if vars(name_space)['unsigned'] is False:
            transaction.sign_with(handle.get_account(chain_id, parser, account_name))
            if sponsor:
                transaction.sponsor_with(handle.get_account(chain_id, parser, sponsor))
            if vars(name_space)['no_broadcast'] is False:
                transaction = transaction.broadcast_to(handle.get_node(chain_id, parser))
        elif vars(name_space)['no_broadcast'] is False:
            parser.error(
                "Use the '--unsigned' option only in combination with the '--no-broadcast' option. Type 'lto lease cancel --help' for more informations ")
        handle.pretty_print(transaction)

    elif vars(name_space)['subparser-name-lease'] == 'list':  # The lease that I'm giving
        node = handle.get_node(chain_id, parser)
        address = handle.get_account(chain_id, parser, account_name).address
        value = node.leaseList(address)
        flag = 0
        for x in value:
            if x['sender'] == address:  # outbound
                print(x['sender'], ':', x['amount'])
                flag +=1
        if flag == 0:
            print("No outbound lease found")

    elif vars(name_space)['subparser-name-lease'] == 'list-inbound':  # The lease that I've received
        node = handle.get_node(chain_id, parser)
        address = handle.get_account(chain_id, parser, account_name).address
        value = node.leaseList(address)
        flag = 0
        for x in value:
            if x['recipient'] == address:  # inbound
                print(x['sender'], ':', x['amount'])
                flag +=1
        if flag == 0:
            print("No inbound lease found")

    else:
        parser.error('Type lto lease --help for instructions')
