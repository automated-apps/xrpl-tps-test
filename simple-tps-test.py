import multiprocessing as mp
import xrpl
from xrpl.clients import JsonRpcClient
import time

def my_func(x):
  #submit a tx
  submit_transaction = xrpl.transaction.submit(transaction=x[0], client=x[1])
  print(submit_transaction)
  print("HERE: ", x[0],x[1])

  print(mp.current_process())
  return submit_transaction

def main(elephant):
  #read 10 blobs from disk into array
  pool = mp.Pool(mp.cpu_count())
  pool = mp.Pool(32)
  result = pool.map(my_func, elephant)

  print(result)



if __name__ == "__main__":

  # Define the Source and Dest wallets
  client = JsonRpcClient("https://s1.ripple.com:51234/")
  destination_algorithm = xrpl.constants.CryptoAlgorithm('secp256k1')

  source_wallet_seed="SECRET"
  source_wallet=xrpl.wallet.Wallet.from_seed(seed=source_wallet_seed, algorithm=destination_algorithm)
  print("Source wallet: ", source_wallet.classic_address)

  destination_wallet_seed="SECRET"
  destination_wallet=xrpl.wallet.Wallet.from_seed(seed=destination_wallet_seed, algorithm=destination_algorithm)
  print("Destination wallet: ", destination_wallet.classic_address)
  
    
  # Create 250 tickets for the source wallet
  ticket_count=150
  client = JsonRpcClient("https://s1.ripple.com:51234/")
  ticket_create_tx = xrpl.models.transactions.TicketCreate(account=source_wallet.classic_address, ticket_count=ticket_count)
  signed_transaction = xrpl.transaction.autofill_and_sign(transaction=ticket_create_tx, wallet=source_wallet, client=client)
  submit_transaction = xrpl.transaction.submit(transaction=signed_transaction, client=client)
  print("Ticket Create transaction result: ", submit_transaction, "\n")
  
  time.sleep(10)

  # Add the reserved ticket numbers to an array
  list_tickets=xrpl.models.requests.AccountObjects(account=source_wallet.classic_address, type="ticket")
  request_tickets=client.request(list_tickets)
  k=1
  sequences=[]
  for i in request_tickets.result['account_objects']:
    print(i['TicketSequence'])
    sequences.append(i['TicketSequence'])
    k=k+1
  print("k: ",k)
  print("Sequences: ", sequences)


  # Create the signed tx as an array
  payment_array=[]
  for i in sequences:
    sequence_number=i
    transaction_amount = "1"
    payment_transaction=xrpl.models.transactions.Payment(account=source_wallet.classic_address, amount=transaction_amount, destination=destination_wallet.classic_address, ticket_sequence=sequence_number, sequence=0, last_ledger_sequence=85876379)
    signed_transaction = xrpl.transaction.autofill_and_sign(transaction=payment_transaction, wallet=source_wallet, client=client)
    payment_array.append([signed_transaction,client])
    print("Completed signing ", i, " of 250")

  # Submit the signed transactions all at once
  main(payment_array)