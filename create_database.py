import sqlite3  
from werkzeug.security import generate_password_hash  
  
# 连接到SQLite数据库（如果数据库不存在，它将被创建）  
conn = sqlite3.connect('database.db')  
cursor = conn.cursor()  
  
# 创建用户表  
cursor.execute('''  
CREATE TABLE IF NOT EXISTS users (  
    id INTEGER PRIMARY KEY AUTOINCREMENT,  
    username TEXT NOT NULL UNIQUE,  
    password TEXT NOT NULL  
)  
''')  
  
# 插入示例用户（使用哈希密码）  
# 注意：在实际应用中，密码不应该硬编码在代码中，这里只是为了示例  
example_users = [  
    {'username': 'admin', 'password': generate_password_hash('admin_password', method='pbkdf2:sha256')},  
    {'username': 'user1', 'password': generate_password_hash('user1_password', method='pbkdf2:sha256')}  
]  
  
for user in example_users:  
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (user['username'], user['password']))  
  
# 提交事务  
conn.commit()  
  
# 关闭连接  
conn.close()  
  
print("Database and table created with example users.")