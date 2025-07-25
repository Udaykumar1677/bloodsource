CREATE DATABASE IF NOT EXISTS bloodsource;
USE bloodsource;

CREATE TABLE IF NOT EXISTS donors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    blood_type VARCHAR(10),
    contact VARCHAR(15),
    city VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    blood_type VARCHAR(10),
    contact VARCHAR(15),
    city VARCHAR(50),
    reason TEXT
);

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blood_banks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            available_groups TEXT NOT NULL,
            units TEXT NOT NULL,
            location TEXT NOT NULL
        )
    ''')
