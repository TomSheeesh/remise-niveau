from flask import Flask, jsonify
import sqlite3

# --- Création de la base en mémoire ---
conn = sqlite3.connect(':memory:', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE customers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT,
    nbr_order INTEGER
)
''')
conn.commit()

clients = [
    ('Gaetan Dupont', 'gaetan.dupont@example.com', '0600000001', 3),
    ('Alice Martin', 'alice.martin@example.com', '0600000002', 5),
    ('Bob Bernard', 'bob.bernard@example.com', '0600000003', 2),
    ('Claire Petit', 'claire.petit@example.com', '0600000004', 7),
    ('David Moreau', 'david.moreau@example.com', '0600000005', 1),
    ('Emma Laurent', 'emma.laurent@example.com', '0600000006', 4),
    ('Franck Leroy', 'franck.leroy@example.com', '0600000007', 2),
    ('Gisele Dubois', 'gisele.dubois@example.com', '0600000008', 6),
    ('Hugo Fabre', 'hugo.fabre@example.com', '0600000009', 3),
    ('Ines Richard', 'ines.richard@example.com', '0600000010', 5)
]

cursor.executemany('''
INSERT INTO customers (name, email, phone, nbr_order)
VALUES (?, ?, ?, ?)
''', clients)
conn.commit()


app = Flask(__name__)

@app.route('/')
def home():
    return "API en cours de fonctionnement !"

@app.route('/customers')
def get_customers():
    cursor.execute("SELECT id, name, email, phone, nbr_order FROM customers")
    rows = cursor.fetchall()
    
    customers = []
    for row in rows:
        customers.append({
            'id': row[0],
            'name': row[1],
            'email': row[2],
            'phone': row[3],
            'nbr_order': row[4]
        })
    
    return jsonify(customers)

### Code en dessous pour ajouter la fonctionnalité de pouvoir choisir un ID spécifique 

@app.route('/customers/<int:id>')
def get_id():
    cursor.execute('SELECT * FROM customers WHERE id=?',(id,))
    row=cursor.fetchone()
    if row is None:
        return "Error 404"
    customer = {
    'id': row[0],
    'name': row[1],
    'email': row[2],
    'phone': row[3],
    'nbr_order': row[4]
}
    return jsonify(customer)

if __name__ == '__main__':
    app.run(debug=True)
