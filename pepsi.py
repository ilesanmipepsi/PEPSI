import hashlib
import time
import json
import secrets

class PepsiCoin:
    def __init__(self):
        self.chain = [self.create_genesis()]
        self.difficulty = 4
        self.pending_transactions = []
        self.wallets = {}

    def create_genesis(self):
        return {"index": 0, "prev": "0", "tx": ["Genesis Block - Let there be $PEPSI"], 
                "miner": "Satoshi", "hash": "0000pepsi", "time": time.time()}

    def create_wallet(self, name):
        wallet = {
            "name": name,
            "address": hashlib.sha256(name.encode()).hexdigest()[:16],
            "balance": 69420069 if name == "PeterAkintade" else 0
        }
        self.wallets[name] = wallet
        return wallet

    def add_transaction(self, sender, recipient, amount, memo="to the moon fr fr 🥤"):
        self.pending_transactions.append({
            "from": sender,
            "to": recipient,
            "amount": amount,
            "memo": memo,
            "time": time.time()
        })
        print(f"🚀 Tx: {sender} → {recipient} | {amount} $PEPSI | {memo}")

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
        
        print(f"⛏️ Mining Block {block['index']}...")
        target = "0" * self.difficulty
        while True:
            h = hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()
            if h.startswith(target):
                block["hash"] = h
                break
            block["nonce"] += 1
        
        self.chain.append(block)
        self.pending_transactions = []
        print(f"✅ Block {block['index']} mined by {miner}! Hash: {h[:20]}...")

    def show_balance(self, name):
        wallet = self.wallets.get(name)
        if wallet:
            print(f"💰 {name}'s balance: {wallet['balance']} $PEPSI")

# === RUN ===
if __name__ == "__main__":
    pepsi = PepsiCoin()
    peter = pepsi.create_wallet("PeterAkintade")
    grok = pepsi.create_wallet("GrokArmy")
    
    pepsi.add_transaction("Genesis", "PeterAkintade", 69420069, "Founder bag")
    pepsi.mine_block("PeterAkintade")
    
    pepsi.add_transaction("PeterAkintade", "GrokArmy", 4206900, "AI raid fund")
    pepsi.mine_block("GrokArmy")
    
    pepsi.show_balance("PeterAkintade")
    pepsi.show_balance("GrokArmy")
    
    print("\n=== $PEPSI LIVE CHAIN ===")
    for b in pepsi.chain:
        print(f"Block #{b['index']} | {b['hash'][:16]}... | Miner: {b['miner']}")
