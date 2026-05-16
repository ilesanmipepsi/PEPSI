import hashlib
import time
import json
import secrets

class PepsiCoin:
    def __init__(self):
        self.chain = [self.create_genesis()]
        self.difficulty = 4
        self.pending_transactions = []

    def create_genesis(self):
        return {"index": 0, "prev": "0", "tx": ["Genesis Block - Let there be $PEPSI"], 
                "miner": "Satoshi", "hash": "0000pepsi genesis", "time": time.time()}

    def create_wallet(self, name):
        return {
            "name": name,
            "address": hashlib.sha256(name.encode()).hexdigest()[:16],
            "balance": 0
        }

    def add_transaction(self, sender, recipient, amount, memo="to the moon fr fr 🥤"):
        self.pending_transactions.append({
            "from": sender,
            "to": recipient,
            "amount": amount,
            "memo": memo,
            "time": time.time()
        })
        print(f"🚀 Transaction: {sender} → {recipient} | {amount} $PEPSI")

    def mine_block(self, miner):
        if not self.pending_transactions:
            print("Nothing to mine")
            return
        last_block = self.chain[-1]
        block = {
            "index": len(self.chain),
            "prev": last_block["hash"],
            "tx": self.pending_transactions[:],
            "miner": miner,
            "time": time.time(),
            "nonce": 0
        }
        
        print(f"⛏️ Mining $PEPSI Block {block['index']}...")
        target = "0" * self.difficulty
        while True:
            block_str = json.dumps(block, sort_keys=True).encode()
            block_hash = hashlib.sha256(block_str).hexdigest()
            if block_hash.startswith(target):
                block["hash"] = block_hash
                break
            block["nonce"] += 1
        
        self.chain.append(block)
        self.pending_transactions = []
        print(f"✅ Block {block['index']} mined by {miner}! Hash: {block_hash[:20]}...")

# === RUN IT ===
if __name__ == "__main__":
    pepsi = PepsiCoin()
    peter = pepsi.create_wallet("PeterAkintade")
    grok = pepsi.create_wallet("GrokArmy")
    
    pepsi.add_transaction("Genesis", peter["name"], 69420069, "Founder bag + war chest")
    pepsi.mine_block("PeterAkintade")
    
    pepsi.add_transaction(peter["name"], grok["name"], 4206900, "For the AI raids")
    pepsi.mine_block("GrokArmy")
    
    print("\n=== $PEPSI BLOCKCHAIN ===")
    for block in pepsi.chain:
        print(f"Block #{block['index']} | Hash: {block['hash'][:16]}... | Miner: {block['miner']}")
