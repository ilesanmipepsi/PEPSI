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
        return {"index": 0, "prev": "0", "tx": ["Genesis Block - Let there be $PEPSI 🥤"], 
                "miner": "Satoshi", "hash": "0000pepsi", "time": time.time()}

    def load_chain(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.chain = data.get("chain", [self.create_genesis()])
                    self.wallets = data.get("wallets", {})
            except:
                self.chain = [self.create_genesis()]
        else:
            self.chain = [self.create_genesis()]

    def save_chain(self):
        with open(self.filename, 'w') as f:
            json.dump({"chain": self.chain, "wallets": self.wallets}, f, indent=2)

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
            print(f"❌ Insufficient balance")
            return False
        self.pending_transactions.append({"from": sender, "to": recipient, "amount": amount, "memo": memo, "time": time.time()})
        if sender in self.wallets:
            self.wallets[sender]["balance"] -= amount
        if recipient not in self.wallets:
            self.create_wallet(recipient)
        self.wallets[recipient]["balance"] += amount
        print(f"🚀 {sender} → {recipient} | {amount:,} $PEPSI")
        return True

    def mine_block(self, miner="PeterAkintade"):
        if not self.pending_transactions:
            print("Nothing to mine")
            return False
        last = self.chain[-1]
        block = {"index": len(self.chain), "prev": last["hash"], "tx": self.pending_transactions[:], 
                 "miner": miner, "time": time.time(), "nonce": 0}
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

# === DASHBOARD ===
class PepsiHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        html = f"""
        <html><head><title>$PEPSI</title>
        <style>body{{font-family:monospace;background:#000;color:#0f0;padding:20px}} 
        h1{{color:#0ff}} .card{{background:#111;padding:20px;margin:15px;border-radius:12px}}</style>
        </head><body>
        <h1>🥤 $PEPSI LIVE</h1>
        <div class="card"><strong>Total Blocks:</strong> {len(pepsi.chain)}</div>
        <div class="card"><strong>Holders:</strong><pre>"""
        for n, w in sorted(pepsi.wallets.items(), key=lambda x: x[1]['balance'], reverse=True):
            html += f"{n}: {w['balance']:,} $PEPSI\n"
        html += """</pre></div><div class="card"><strong>Recent Blocks:</strong><pre>"""
        for b in pepsi.chain[-8:]:
            html += f"#{b['index']} | {b['hash'][:16]}... | {b['miner']}\n"
        html += """</pre></div><p>Refresh after mining • Shadow mode</p></body></html>"""
        self.wfile.write(html.encode())

if __name__ == "__main__":
    global pepsi
    pepsi = PepsiCoin()
    pepsi.create_wallet("PeterAkintade")
    pepsi.create_wallet("PepsiRaiders")

    try:
        server = HTTPServer(('0.0.0.0', 8000), PepsiHandler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        print("🌐 Dashboard: http://localhost:8000")
    except:
        pass

    print("\n$PEPSI v1.6 Shadow Raider Active 🥤")
    while True:
        print("\n1: Send  2: Mine  3: Status  4: Exit")
        c = input("Choice: ").strip()
        if c == "1":
            s = input("From: ").strip()
            r = input("To: ").strip()
            try: pepsi.add_transaction(s, r, int(input("Amount: ").strip()))
            except: print("Error")
        elif c == "2":
            pepsi.mine_block(input("Miner: ").strip() or "PeterAkintade")
        elif c == "3":
            for n,w in sorted(pepsi.wallets.items(), key=lambda x:x[1]['balance'], reverse=True):
                print(f"{n}: {w['balance']:,}")
        elif c == "4":
            break
