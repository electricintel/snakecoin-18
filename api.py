from flask import Flask
from flask import request

import numpy as np
import os.path

import json
import requests
import hashlib as hasher
import datetime as date
node = Flask(__name__)

# Define what a Snakecoin block is
class Block:
  def __init__(self, index, timestamp, data, previous_hash):
    self.index = index
    self.timestamp = timestamp
    self.data = data
    self.previous_hash = previous_hash
    self.hash = self.hash_block()

  def hash_block(self):
    sha = hasher.sha256()
    sha.update(str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash))
    return sha.hexdigest()

# Generate genesis block
def create_genesis_block():
  # Manually construct a block with
  # index zero and arbitrary previous hash
  return Block(0, date.datetime.now(), {
    "proof-of-work": 9,
    "transactions": None
  }, "0")

# A completely random address of the owner of this node
miner_address = "q3nf394hjg-root-34nf3i4nflkn3oi"
# This node's blockchain copy
blockchain = []

fnames = ("blockchain.npy", "this_nodes_transactions.npy", "peer_nodes.npy")

if os.path.isfile(fnames[0]):
  blockchain = np.load(fnames[0]).tolist()
else:
  blockchain.append(create_genesis_block())

# Store the transactions that
# this node has in a list
this_nodes_transactions = []
if os.path.isfile(fnames[1]):
  this_nodes_transactions = np.load(fnames[1]).tolist()

# Store the url data of every
# other node in the network
# so that we can communicate
# with them
peer_nodes = []
if os.path.isfile(fnames[2]):
  peer_nodes = np.load(fnames[2]).tolist()

# A variable to deciding if we're mining or not
mining = True

@node.route('/txion', methods=['POST'])
def transaction():
  # On each new POST request,
  # we extract the transaction data
  new_txion = request.get_json()
  # Then we add the transaction to our list
  this_nodes_transactions.append(new_txion)
  ## Save
  np.save("this_nodes_transactions.npy", this_nodes_transactions)
  # Because the transaction was successfully
  # submitted, we log it to our console
  print "New transaction"
  print "FROM: {}".format(new_txion['from'].encode('ascii','replace'))
  print "TO: {}".format(new_txion['to'].encode('ascii','replace'))
  print "AMOUNT: {}\n".format(new_txion['amount'])
  # Then we let the client know it worked out
  return "Transaction submission successful\n"

@node.route('/blocks', methods=['GET'])
def get_blocks():
  chain_to_send = blockchain
  # Convert our blocks into dictionaries
  # so we can send them as json objects later
  for i in range(len(chain_to_send)):
    block = chain_to_send[i]
    block_index = str(block.index)
    block_timestamp = str(block.timestamp)
    block_data = str(block.data)
    block_hash = block.hash
    chain_to_send[i] = {
      "index": block_index,
      "timestamp": block_timestamp,
      "data": block_data,
      "hash": block_hash
    }
  chain_to_send = json.dumps(chain_to_send)
  return chain_to_send

def find_new_chains():
  # Get the blockchains of every
  # other node
  other_chains = []
  for node_url in peer_nodes:
    # Get their chains using a GET request
    block = requests.get(node_url + "/blocks").content
    # Convert the JSON object to a Python dictionary
    block = json.loads(block)
    # Add it to our list
    other_chains.append(block)
  return other_chains

def consensus():
  # Get the blocks from other nodes
  other_chains = find_new_chains()
  # If our chain isn't longest,
  # then we store the longest chain
  longest_chain = blockchain
  for chain in other_chains:
    if len(longest_chain) < len(chain):
      longest_chain = chain
  # If the longest chain isn't ours,
  # then we stop mining and set
  # our chain to the longest one
  blockchain = longest_chain

def proof_of_work(last_proof):
  # Create a variable that we will use to find
  # our next proof of work
  incrementor = last_proof + 1
  # Keep incrementing the incrementor until
  # it's equal to a number divisible by 9
  # and the proof of work of the previous
  # block in the chain
  while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
    incrementor += 1
  # Once that number is found,
  # we can return it as a proof
  # of our work
  return incrementor

@node.route('/mine', methods = ['GET'])
def mine():
  # Get the last proof of work
  last_block = blockchain[len(blockchain) - 1]
  last_proof = last_block.data['proof-of-work']
  # Find the proof of work for
  # the current block being mined
  # Note: The program will hang here until a new
  #       proof of work is found
  proof = proof_of_work(last_proof)
  # Once we find a valid proof of work,
  # we know we can mine a block so
  # we reward the miner by adding a transaction
  this_nodes_transactions.append(
    { "from": "network", "to": miner_address, "amount": 1 }
  )
  # Now we can gather the data needed
  # to create the new block
  new_block_data = {
    "proof-of-work": proof,
    "transactions": list(this_nodes_transactions)
  }
  new_block_index = last_block.index + 1
  new_block_timestamp = this_timestamp = date.datetime.now()
  last_block_hash = last_block.hash
  # Empty transaction list
  #this_nodes_transactions[:] = []
  # Now create the
  # new block!
  mined_block = Block(
    new_block_index,
    new_block_timestamp,
    new_block_data,
    last_block_hash
  )
  blockchain.append(mined_block)
  ## Save
  np.save("blockchain.npy", blockchain)
  np.save("this_nodes_transactions.npy", this_nodes_transactions)
  # Let the client know we mined a block
  return json.dumps({
      "index": new_block_index,
      "timestamp": str(new_block_timestamp),
      "data": new_block_data,
      "hash": last_block_hash
  }) + "\n"

@node.route('/ledger', methods = ['GET'])
def ledger():
  # Get the last proof of work
  last_block = blockchain[len(blockchain) - 1]
  return json.dumps({
      "index": last_block.index,
      "timestamp": str(last_block.timestamp),
      "data": last_block.data,
      "hash": last_block.hash
  }) + "\n"

def balance_of(name):
    balance = 0
    if name:
        last_block = blockchain[len(blockchain) - 1]
        data = last_block.data
        transactions = data['transactions']
        if transactions:
            for e in transactions:
                if e['to']==name:
                    balance += e['amount']
                elif e['from']==name:
                    balance -= e['amount']
    return balance

@node.route('/balance',methods=['GET'])
def balance():
    name = str(request.query_string).encode('utf-8')
    if name:
        balance = balance_of(name)
        last_block = blockchain[len(blockchain) - 1]
        return json.dumps({
            "name": name,
            "timestamp": str(last_block.timestamp),
            "balance": balance
        })
    return json.dumps({
        "error": True,
        "message": "Invalid query"
    })

def history_of(name):
    if name:
        last_block = blockchain[len(blockchain) - 1]
        data = last_block.data
        transactions = data['transactions']
        history = []
        if transactions:
            for e in transactions:
                if e['to']==name or e['from']==name:
                    history.append(e)
        return history
    return []

@node.route('/history',methods=['GET'])
def history():
    name = str(request.query_string).encode('utf-8')
    balance = 0
    if name:
        history = history_of(name)
        last_block = blockchain[len(blockchain) - 1]
        return json.dumps({
            "name": name,
            "timestamp": str(last_block.timestamp),
            "history": history
        })
    return json.dumps({
        "error": True,
        "message": "Invalid query"
    })

node.run()
