# Snakecoin Blockchain

## Installation
    sudo python -m pip install flask # Install web server framework
    sudo python -m pip install requests
    sudo python -m pip install -U flask-cors

## Serve
    python api.py

## Operations
1. Create a transaction


    curl "localhost:5000/txion" \
         -H "Content-Type: application/json" \
         -d '{"from": "akjflw", "to":"fjlakdj", "amount": 3}'

2. Mine a new block.


    curl localhost:5000/mine

### Sample of output

```
$ curl "localhost:5000/txion" -H "Content-Type: application/json"          -d '{"from": "akjflw", "to":"fjlakdj", "amount": 3}'
Transaction submission successful

$ curl localhost:5000/mine
{
  "index": 1,
  "data": {
    "transactions": [
      {
        "to": "fjlakdj",
        "amount": 3,
        "from": "akjflw"
      }, {
        "to": "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi", "amount": 1,
        "from": "network"
      }
    ],
    "proof-of-work": 18
  },
  "hash": "177aabf4e05e33746f8b74ed78a8f9e46f0bd130acd6a3f6a150bd4fbd3e2ac9",
  "timestamp": "2019-01-19 15:02:29.453647"
}
```

## Test running blockchain in terminal
    python blockchain.py

### Sample of output
```
Block #1 has been added to the blockchain!
Hash: fa62d1f49bef17955434f1441d81b4835ca7d02159b9c810cc1cc044b5438fbc

Block #2 has been added to the blockchain!
Hash: f3e7049d8772b4fde079f7346c465253af53063e61593a7b6a46db6a07ab6710

Block #3 has been added to the blockchain!
Hash: 0c6f77df6e85d4a5fb3d684bf40f5db21c3e2cc8e454d67563e6d89f09595748

Block #4 has been added to the blockchain!
Hash: 26ebfcf033bd095bb4d32208aee9c77c2b7063262609e3a87c32d2093914947f

Block #5 has been added to the blockchain!
Hash: 4eb55766d3bd3d7f73c3321fd00d87e4e1bbf9cf6d69b632f10a49304cbe0141

Block #6 has been added to the blockchain!
Hash: d94ee20e5c936e73f36f0a12a33a823493c6a32166b1566c9fe0696976d0680a

Block #7 has been added to the blockchain!
Hash: 9dc2cd24a249bfa3ecdeb9a2eb7a538484f139c4504b4a34228520d4246eac37

Block #8 has been added to the blockchain!
Hash: 322c674511c910b5ae10fb112857a59942f6100b0327f960d982f5b75a4c6021

Block #9 has been added to the blockchain!
Hash: 8c88f2e84125173f234c9a03625471577a63739f97f00dd30e6ad91e31c3cc93

Block #10 has been added to the blockchain!
Hash: 9717c5782518e617a21ed90358079a4ff2706e119cfa3c1d65758d158660738a

Block #11 has been added to the blockchain!
Hash: e941ff0a778736baf98958445a762a9ca587a2e2916440240fe9c0c2a3d8ae3c

Block #12 has been added to the blockchain!
Hash: bf2205966a4a6a57166c6a87e5e48e9351fe4e568a2691df7c8470b83b4e3a43

Block #13 has been added to the blockchain!
Hash: 081cf5369a0505bbe35c06d41a5d9f7d22f114dbbad15e0f9aa0d6398c2fe078

Block #14 has been added to the blockchain!
Hash: 6690e09f457ee5767ef6a391d8b409244f82913d1cc321d198c9aa4e3b581bd4

Block #15 has been added to the blockchain!
Hash: 4bd8be2b2452a9c2a6cb5365693d3f65a3dfe5c74e75abb218f198913e7db7db

Block #16 has been added to the blockchain!
Hash: 7eb2a33042f12f7b051dbdcdc98c6693fc8e823d04cfeb7d12c7937d8e211fab

Block #17 has been added to the blockchain!
Hash: d72fd44f6d4455788e3179dcd816294116393f8e648af4192e5ac4f7eb0cff38

Block #18 has been added to the blockchain!
Hash: 8e528c1f50a5772aa9ff9a4b5bfe684dd5625a35153bed54a3a40f5ae431ae39

Block #19 has been added to the blockchain!
Hash: 7408e8ef0b81bbdaea1f77dfd6ba49b82aabc82a464d0d2df7272ca30799391c

Block #20 has been added to the blockchain!
Hash: a0cac6463ed75e2fc07d46da3d54c9161b3cce609ec8c3ec8371387bfdf0c956
```

## Some commands that might be useful in MacOS
    xcode-select --install
    sudo easy_install pip
    brew install python

## Reference
* Let’s Build the Tiniest Blockchain, https://medium.com/crypto-currently/lets-build-the-tiniest-blockchain-e70965a248b
* Let’s Make the Tiniest Blockchain Bigger - https://medium.com/crypto-currently/lets-make-the-tiniest-blockchain-bigger-ac360a328f4d
* Bitcoin whitepaper, https://bitcoin.org/bitcoin.pdf
