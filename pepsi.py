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
        return {
            "index": 0, 
            "prev": "0", 
            "tx": ["Genesis Block - Let there be $PEPSI 🥤"], 
            "miner": "Satoshi", 
            "hash": "0000pepsi", 
            "time": time.time()
        }

    def create_wallet(self, name):
        wallet = {
            "name": name,
            "address": hashlib.sha256(name.encode()).hexdigest()[:16],
            "balance": 69420069 if name == "PeterAkintade" else 0
        }
        self.wallets[name] = wallet
        print(f"🆕 Wallet created: {name} | Address: {wallet['address']}")
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
        if recipient in self.wallets:
            self.wallets[recipient]["balance"] += amount
        else:
            self.create_wallet(recipient)
            self.wallets[recipient]["balance"] += amount
            
        print(f"🚀 Tx: {sender} → {recipient} | {amount} $PEPSI | {memo}")
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
        
        print(f"⛏️ Mining $PEPSI Block {block['index']}... (Difficulty: {self.difficulty})")
        target = "0" * self.difficulty
        start_time = time.time()
        
        while True:
            h = hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()
            if h.startswith(target):
                block["hash"] = h
                break
            block["nonce"] += 1
            # Auto adjust difficulty every 3 blocks
            if block["index"] % 3 == 0 and block["index"] > 0:
                self.difficulty = max(3, self.difficulty + 1)
        
        self.chain.append(block)
        self.pending_transactions = []
        print(f"✅ Block {block['index']} mined by {miner}! Hash: {h[:20]}...")
        print(f"⏱️  Took {time.time() - start_time:.2f} seconds")

    def show_balance(self, name):
        wallet = self.wallets.get(name)
        if wallet:
            print(f"💰 {name}'s balance: {wallet['balance']:,} $PEPSI")
        else:
            print(f"Wallet {name} not found")

    def show_chain(self):
        print("\n=== $PEPSI LIVE BLOCKCHAIN ===")
        for b in self.chain:
            print(f"Block #{b['index']} | Hash: {b['hash'][:16]}... | Miner: {b['miner']}")
            if b.get('tx') and isinstance(b['tx'], list) and len(b['tx']) > 0 and isinstance(b['tx'][0], dict):
                for tx in b['tx']:
                    print(f"   └─ {tx['from']} → {tx['to']} | {tx['amount']} $PEPSI | {tx.get('memo','')}")
            elif b.get('tx'):
                print(f"   └─ Genesis: {b['tx']}")

# === RUN THE COIN ===
if __name__ == "__main__":
    pepsi = PepsiCoin()
    
    peter = pepsi.create_wallet("PeterAkintade")
    raiders = pepsi.create_wallet("PepsiRaiders")
    
    pepsi.add_transaction("Genesis", "PeterAkintade", 69420069, "Founder bag + jet fuel")
    pepsi.mine_block("PeterAkintade")
    
    pepsi.add_transaction("PeterAkintade", "PepsiRaiders", 4206900, "Raid fund")
    pepsi.mine_block("PeterAkintade")
    
    pepsi.add_transaction("PeterAkintade", "PepsiRaiders", 2500000, "More war chest")
    pepsi.mine_block("PeterAkintade")
    
    pepsi.show_balance("PeterAkintade")
    pepsi.show_balance("PepsiRaiders")
    pepsi.show_chain()
    
    print("\n$PEPSI v0.6 Stealth Raider Edition is LIVE 🥤💣")
