import hashlib
import time
import json
import secrets
import os

class PepsiCoin:
    def __init__(self, filename="pepsi_chain.json"):
        self.filename = filename
        self.chain = []
        self.difficulty = 4
        self.pending_transactions = []
        self.wallets = {}
        self.load_chain()

    def create_genesis(self):
        return {
            "index": 0, 
            "prev": "0", 
            "tx": ["Genesis Block - Let there be $PEPSI 🥤"], 
            "miner": "Satoshi", 
            "hash": "0000pepsi", 
            "time": time.time()
        }

    def load_chain(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.chain = data.get("chain", [self.create_genesis()])
                    self.wallets = data.get("wallets", {})
                print(f"✅ Loaded existing chain with {len(self.chain)} blocks")
            except:
                self.chain = [self.create_genesis()]
        else:
            self.chain = [self.create_genesis()]

    def save_chain(self):
        data = {
            "chain": self.chain,
            "wallets": self.wallets
        }
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)
        print("💾 Chain saved to pepsi_chain.json")

    def create_wallet(self, name):
        if name in self.wallets:
            print(f"✅ Wallet {name} already exists")
            return self.wallets[name]
        
        wallet = {
            "name": name,
            "address": hashlib.sha256(name.encode()).hexdigest()[:16],
            "balance": 69420069 if name == "PeterAkintade" else 0
        }
        self.wallets[name] = wallet
        print(f"🆕 New wallet: {name} | Address: {wallet['address']}")
        return wallet

    def add_transaction(self, sender, recipient, amount, memo="to the moon fr fr 🥤"):
        if sender in self.wallets and self.wallets[sender]["balance"] < amount:
            print(f"❌ Insufficient balance for {sender}")
            return False
        
        self.pending_transactions.append({
            "from": sender,
            "to": recipient,
            "amount": amount,
            "memo": memo,
            "time": time.time()
        })
        
        if sender in self.wallets:
            self.wallets[sender]["balance"] -= amount
        if recipient not in self.wallets:
            self.create_wallet(recipient)
        self.wallets[recipient]["balance"] += amount
            
        print(f"🚀 Tx: {sender} → {recipient} | {amount:,} $PEPSI | {memo}")
        return True

    def mine_block(self, miner):
        if not self.pending_transactions:
            print("Nothing to mine")
            return
        
        last = self.chain[-1]
        block = {
            "index": len(self.chain),
            "prev": last["hash"],
            "tx": self.pending_transactions[:],
            "miner": miner,
            "time": time.time(),
            "nonce": 0
        }
        
        print(f"⛏️ Mining Block {block['index']} (Difficulty: {self.difficulty})...")
        target = "0" * self.difficulty
        start = time.time()
        
        while True:
            h = hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()
            if h.startswith(target):
                block["hash"] = h
                break
            block["nonce"] += 1
        
        self.chain.append(block)
        self.pending_transactions = []
        print(f"✅ Block {block['index']} mined by {miner}! Hash: {h[:20]}...")
        print(f"⏱️ Time: {time.time() - start:.2f} seconds")
        
        self.save_chain()

    def show_balance(self, name):
        wallet = self.wallets.get(name)
        if wallet:
            print(f"💰 {name}: {wallet['balance']:,} $PEPSI")
        else:
            print(f"Wallet {name} not found")

    def show
