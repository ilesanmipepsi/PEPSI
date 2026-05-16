import hashlib
import time
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

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
                print(f"✅ Loaded {len(self.chain)} blocks")
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
        print(f"🚀 {sender} → {recipient} | {amount:,} $PEPSI")
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
        
        target = "0" * self.difficulty
        while True:
            h = hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()
            if h.startswith(target):
                block["hash"] = h
                break
            block["nonce"] += 1
        
        self.chain.append(block)
        self.pending_transactions = []
        self.save_chain()
        print(f"✅ Block {block['index']} mined by {miner}!")
        return True

# === BEAUTIFUL WEB DASHBOARD ===
class PepsiHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        html = f"""
        <html>
        <head>
            <title>$PEPSI Live</title>
            <style>
                body {{ font-family: monospace; background: #0a0a0a; color: #00ff88; padding: 20px; margin: 0; }}
                h1 {{ color: #00ffff; text-align: center; }}
                .card {{ background: #111111; padding: 18px; border-radius: 12px; margin: 15px 0; box-shadow: 0 0 10px rgba(0,255,100,0.2); }}
                pre {{ background: #000; padding: 15px; border-radius: 8px; overflow-x: auto; }}
                .refresh {{ color: #00ffcc; font-size: 0.9em; }}
            </style>
        </head>
        <body>
        <h1>🥤 $PEPSI LIVE BLOCKCHAIN</h1>
        
        <div class="card">
            <strong>Total Blocks:</strong> {len(pepsi.chain)}
        </div>
        
        <div class="card">
            <strong>Holders:</strong><br>
            <pre>"""
        
        for name, w in sorted(pepsi.wallets.items(), key=lambda x: x[1]['balance'], reverse=True):
            html += f"{name}: {w['balance']:,} $PEPSI\n"
        
        html += """</pre>
        </div>
        
        <div class="card">
            <strong>Recent Blocks:</strong><br>
            <pre>"""
        
        for b in pepsi.chain[-8:]:
            html += f"#{b['index']} | {b['hash'][:16]}... | {b['miner']}\n"
        
        html += """</pre>
        </div>
        
        <p class="refresh">Refresh this page after mining • $PEPSI v1.3 • Built on mobile phone 💯</p>
        </body>
        </html>"""
        self.wfile.write(html.encode())

# === MAIN ===
if __name__ == "__main__":
    global pepsi
    pepsi = PepsiCoin()
    
    pepsi.create_wallet("PeterAkintade")
    pepsi.create_wallet("PepsiRaiders")
    
    print("\n🚀 $PEPSI v1.3 Polished Raider Edition")
    
    try:
        server = HTTPServer(('0.0.0.0', 8000), PepsiHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        print("🌐 Dashboard live at → http://localhost:8000")
        print("                   → http://127.0.0.1:8000")
    except Exception as e:
        print("Web server note:", str(e)[:80])

    # Initial setup
    if pepsi.wallets["PepsiRaiders"]["balance"] < 10000000:
        pepsi.add_transaction("PeterAkintade", "PepsiRaiders", 10000000)
        pepsi.mine_block("PeterAkintade")

    # Interactive commands
    while True:
        print("\n1: Send   2: Mine   3: Status   4: Exit")
        choice = input("Choice: ").strip()
        
        if choice == "1":
            s = input("From: ").strip()
            r = input("To: ").strip()
            try:
                amt = int(input("Amount: ").strip())
                pepsi.add_transaction(s, r, amt)
            except:
                print("Invalid amount")
        elif choice == "2":
            m = input("Miner (default: PeterAkintade): ").strip() or "PeterAkintade"
            pepsi.mine_block(m)
        elif choice == "3":
            for name, w in sorted(pepsi.wallets.items(), key=lambda x: x[1]['balance'], reverse=True):
                print(f"{name}: {w['balance']:,} $PEPSI")
        elif choice == "4":
            print("👋 $PEPSI chain saved securely.")
            break
