CREATE TABLE Expenses (
    expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
    id INTEGER,
    amount DECIMAL(10, 2),
    category VARCHAR(255) CHECK (category IN ('personal expenses', 'leisure', 'investment')),
    date DATE,
    FOREIGN KEY (id) REFERENCES user(id)
);

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
);

CREATE TABLE Income (
    income_id INTEGER PRIMARY KEY AUTOINCREMENT,
    id INTEGER,
    amount DECIMAL(10, 2), 
    date DATE,
    FOREIGN KEY (id) REFERENCES user(id)
);

CREATE TABLE bank (
    bank_id INTEGER PRIMARY KEY AUTOINCREMENT,
    id INTEGER,
    amount DECIMAL(10, 2),
    FOREIGN KEY (id) REFERENCES user(id)
);

CREATE TABLE investments (
    investment_id INTEGER PRIMARY KEY,
    id INTEGER,
    type CHECK (type IN ('Stocks', 'Real Estate', 'Mutual Funds', 'Bonds')),
    amount DECIMAL(10, 2),
    return DECIMAL(10, 2),
    start_date DATE,
    end_date DATE,
    duration INT,
    FOREIGN KEY (id) REFERENCES user(id)
);