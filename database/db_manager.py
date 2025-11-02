import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent

def get_connection():
    """

    Connect to database file.

    """

    return sqlite3.connect(DB_PATH)

def init_db():
    """
    
    Db dosyası içinde eğer gerekli tablolar yoksa tabloları oluşturur.

    """

    conn = get_connection()
    cursor = conn.cursor()

    #Portfolio table
    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS portfolio(id INTEGER PRIMARY KEY AUTOINCREMENT,
                   symbol TEXT NOT NULL,
                   cost REAL NOT NULL,
                   amount REAL NOT NULL
                   )


    """)

    #Watch list groups

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS watchlist_groups (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL
                   )

""")
    
    #watch list items

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS watchlist_items (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   group_id INTEGER,
                   symbol TEXT,
                   FOREIGN KEY (group_id) REFERNCES watchlist_groups(id)
                   )


""")
    
    conn.commit()
    conn.close()





#Portfolio Options.

def add_stock(symbol,cost,amount):
    """
    Add new stock
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO portfolio (symbol,cost,amount) VALUES (?,?,?)")
    conn.commit()
    conn.close()


def get_all_portfolio():
    """
    See all stocks of portfolio
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT symbol,cost,amount FROM porftolio")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Watchlists options.
def add_watchlist(name):
    """
    Create watchlist

    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO watchlist_groups (name) VALUES (?)",(name,))
    conn.commit()
    conn.close()


def get_watchlists():
    """
    See all watchlists
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM watchlist_groups")
    data = cursor.fetchall()
    conn.close()
    return data

def add_symbol_to_watchlist(group_id, symbol):
    """Add a new stock to watchlist."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO watchlist_items (group_id, symbol) VALUES (?, ?)", (group_id, symbol))
    conn.commit()
    conn.close()

def get_symbols_in_watchlist(group_id):
    """see all watchlist."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT symbol FROM watchlist_items WHERE group_id = ?", (group_id,))
    data = [row[0] for row in cur.fetchall()]
    conn.close()
    return data