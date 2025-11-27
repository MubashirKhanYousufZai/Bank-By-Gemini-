import sqlite3

def get_db_connection():
    conn = sqlite3.connect('bank.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            name TEXT PRIMARY KEY,
            balance REAL NOT NULL
        );
    """)
    # Check if table is empty
    c.execute("SELECT COUNT(*) FROM accounts")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", ('Ali', 5000))
        c.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", ('Me', 1000))
        c.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", ('Fatima', 2500))
    conn.commit()
    conn.close()

def get_accounts():
    conn = get_db_connection()
    accounts = conn.execute('SELECT * FROM accounts').fetchall()
    conn.close()
    return {acc['name']: {'balance': acc['balance']} for acc in accounts}

def get_account(name: str):
    conn = get_db_connection()
    account = conn.execute('SELECT * FROM accounts WHERE name = ?', (name,)).fetchone()
    conn.close()
    return account

def update_balances(sender: str, receiver: str, amount: float):
    conn = get_db_connection()
    try:
        # Start transaction
        conn.execute('BEGIN')
        
        sender_acc = conn.execute('SELECT balance FROM accounts WHERE name = ?', (sender,)).fetchone()
        if sender_acc is None:
            raise ValueError(f"Sender '{sender}' not found.")
        if sender_acc['balance'] < amount:
            raise ValueError("Insufficient funds.")

        receiver_acc = conn.execute('SELECT balance FROM accounts WHERE name = ?', (receiver,)).fetchone()
        if receiver_acc is None:
            raise ValueError(f"Receiver '{receiver}' not found.")

        conn.execute('UPDATE accounts SET balance = balance - ? WHERE name = ?', (amount, sender))
        conn.execute('UPDATE accounts SET balance = balance + ? WHERE name = ?', (amount, receiver))
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# Initialize the database on startup
init_db()
