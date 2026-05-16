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
                print(f"✅ Loaded {len(self.chain)} blocks from disk")
            except:
                self.chain = [self.create_genesis()]
        else:
            self.chain = [self.create_genesis()]

    def save_chain(self):
        data = {"chain": self.chain, "wallets": self.wallets}
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)

    def create_wallet(self, name):
        if name in self.wallets:
            return self.wallets[name]
        
        wallet = {
            "name": name,
            "address": hashlib.sha256(name.encode()).hexdigest()[:16],
            "balance": 69420069 if name == "PeterAkintade" else 0
        }
        self.wallets[name] = wallet
        print(f"🆕 Wallet: {name} | Addr: {wallet['address']}")
        return wallet

    def add_transaction(self, sender, recipient, amount, memo="to the moon fr fr 🥤"):
        if sender in self.wallets and self.wallets[sender]["balance"] < amount:
            print(f"❌ Not enough $PEPSI in {sender}")
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
        
        print(f"🚀 Sent {amount:,} $PEPSI → {recipient}")
        return True

    def mine_block(self, miner):
        if not self.pending_transactions:
            print("No transactions to mine")
            return False
        
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
        print(f"✅ Block mined! Hash: {h[:20]}...")
        print(f"⏱️ Took {time.time() - start:.2f}s")
        
        self.save_chain()
        return True

    def show_balance(self, name):
        w = self.wallets.get(name)
        if w:
            print(f"💰 {name}: {w['balance']:,} $PEPSI")
        else:
            print(f"Wallet {name} not found")

    def show_chain(self):
        print("\n=== $PEPSI BLOCKCHAIN ===")
        for b in self.chain:
            print(f"Block #{b['index']} | {b['hash'][:16]}... | Miner: {b['miner']}")
            if isinstance(b.get('tx'), list) and len(b['tx']) > 0 and isinstance(b['tx'][0], dict):
                for tx in b['tx']:
                    print(f"   └─ {tx['from']} → {tx['to']} | {tx['amount']:,} $PEPSI")

    def show_all(self):
        print("\n💎 $PEPSI HOLDERS:")
        for name, w in sorted(self.wallets.items(), key=lambda x: x[1]['balance'], reverse=True):
            print(f"   {name}: {w['balance']:,} $PEPSI")

# === INTERACTIVE MODE ===
if __name__ == "__main__":
    pepsi = PepsiCoin()
    
    pepsi.create_wallet("PeterAkintade")
    pepsi.create_wallet("PepsiRaiders")
    
    print("\n🚀 $PEPSI v0.8 Command Raider Edition")
    print("Type commands or run transactions below:\n")
    
    pepsi.add_transaction("Genesis", "PeterAkintade", 69420069, "Founder bag")
    pepsi.mine_block("PeterAkintade")
    
    pepsi.add_transaction("PeterAkintade", "PepsiRaiders", 4206900, "Raid fund")
    pepsi.mine_block("PeterAkintade")
    
    pepsi.show_all()
    pepsi.show_chain()
    
    print("\n$PEPSI is now persistent and interactive 🥤💣")
    print("You can keep adding transactions and mining blocks!")
