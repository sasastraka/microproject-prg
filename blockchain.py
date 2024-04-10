import hashlib
import json
from time import time


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        
        # Vytvoření genesis bloku
        self.new_block(previous_hash='1', proof=100)
    
    def new_block(self, proof, previous_hash=None):
        """
        Vytvoří nový blok v blockchainu
        
        :param proof: <int> Proof of work
        :param previous_hash: (Optional) <str> Hash předchozího bloku
        :return: <dict> Nový blok
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        
        self.current_transactions = []
        
        self.chain.append(block)
        return block
    
    def new_transaction(self, sender, recipient, amount):
        """
        Vytvoří novou transakci
        
        :param sender: <str> Adresa odesílatele
        :param recipient: <str> Adresa příjemce
        :param amount: <int> Množství
        :return: <int> Index bloku obsahující tuto transakci
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        
        return self.last_block['index'] + 1
    
    @staticmethod
    def hash(block):
        """
        Vytvoří SHA-256 hash bloku
        
        :param block: <dict> Blok
        :return: <str> Hash hodnota
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    @property
    def last_block(self):
        return self.chain[-1]
    
    
blockchain = Blockchain()

blockchain.new_transaction("Alice", "Bob", 5)
blockchain.new_transaction("Bob", "Charlie", 10)
blockchain.new_transaction("Charlie", "Alice", 7)

last_block = blockchain.last_block
last_proof = last_block['proof']
proof = 100 


blockchain.new_block(proof, blockchain.hash(last_block))

print(json.dumps(blockchain.chain, indent=4))
