CREATE TABLE Users (
  Userid INT AUTO_INCREMENT,
  Fullname VARCHAR(50) NOT NULL,
  phone_number VARCHAR(15) NOT NULL,
  account_type ENUM('Personal','business','agent') NOT NULL,
  PRIMARY KEY (Userid),
  UNIQUE KEY (phone_number)
);

CREATE TABLE Categories (
  categoryid INT AUTO_INCREMENT,
  category_name VARCHAR(20) NOT NULL,
  category_code VARCHAR(10),
  description TEXT,
  PRIMARY KEY (categoryid),
  UNIQUE KEY (category_code)
);

CREATE TABLE Transactions (
  Transaction_id INT AUTO_INCREMENT,
  categoryid INT,
  Financial_Transaction_id VARCHAR(20),
  fee DECIMAL(10,2) NOT NULL DEFAULT 0,
  Amount DECIMAL(12,2) NOT NULL,
  Status ENUM('Pending','failed','Completed') DEFAULT 'Pending',
  Currency VARCHAR(3) DEFAULT 'RWF',
  Transaction_date DATETIME NOT NULL,
  raw_body TEXT NOT NULL,
  PRIMARY KEY (Transaction_id),
  FOREIGN KEY (categoryid) REFERENCES Categories(categoryid),
  CHECK (Amount > 0)
);

CREATE TABLE System_Logs (
  log_id INT AUTO_INCREMENT,
  transaction_id INT NOT NULL,
  process_stage ENUM('Initiated','Validated','Processing','Completed') NOT NULL,
  log_message TEXT,
  log_status ENUM('Info','Success','Warning','Error') NOT NULL,
  PRIMARY KEY (log_id),
  FOREIGN KEY (transaction_id) REFERENCES Transactions(Transaction_id)
);

CREATE TABLE Transaction_participants (
  Participant_id INT AUTO_INCREMENT,
  Userid INT NOT NULL,
  Transactionid INT NOT NULL,
  role ENUM('sender', 'receiver') NOT NULL,
  PRIMARY KEY (Participant_id),
  FOREIGN KEY (Userid) REFERENCES Users(Userid),
  FOREIGN KEY (Transactionid) REFERENCES Transactions(Transaction_id),
  UNIQUE KEY (Transactionid, role)
);


-- ============================
-- 1. Users
-- ============================
INSERT INTO Users (Fullname, phone_number, account_type) VALUES
('Aline Uwase', '250788123456', 'Personal'),
('Eric Niyonzima', '250788234567', 'Personal'),
('Grace Mukamana', '250788345678', 'business'),
('Jean Bosco Habimana', '250788456789', 'Personal'),
('Divine Store Ltd', '250788567890', 'agent');

-- ============================
-- 2. Categories
-- ============================
INSERT INTO Categories (category_name, category_code, description) VALUES
('Airtime Purchase', 'AIRTM', 'Purchase of mobile airtime credit'),
('P2P Transfer', 'P2P', 'Person-to-person money transfer'),
('Bill Payment', 'BILL', 'Utility or service bill payment'),
('Cash Withdrawal', 'WDRWL', 'Cash withdrawal via agent'),
('Merchant Payment', 'MERCH', 'Payment to a registered merchant/business');

-- ============================
-- 3. Transactions
-- (categoryid 1-5 references Categories inserted above)
-- ============================
INSERT INTO Transactions (categoryid, Financial_Transaction_id, fee, Amount, Status, Currency, Transaction_date, raw_body) VALUES
(2, 'FTX10023456', 100, 5000.00, 'Completed', 'RWF', '2026-09-01 09:15:00', 'You have sent 5000 RWF to Eric Niyonzima. Fee 100 RWF. TxId: FTX10023456'),
(1, 'FTX10023457', 0, 1000.00, 'Completed', 'RWF', '2026-09-02 14:30:00', 'You have purchased 1000 RWF airtime. TxId: FTX10023457'),
(3, 'FTX10023458', 200, 15000.00, 'Completed', 'RWF', '2026-09-03 11:00:00', 'You have paid 15000 RWF for electricity bill. Fee 200 RWF. TxId: FTX10023458'),
(4, 'FTX10023459', 500, 20000.00, 'Pending', 'RWF', '2026-09-04 16:45:00', 'Withdrawal of 20000 RWF requested via agent. Fee 500 RWF. TxId: FTX10023459'),
(5, 'FTX10023460', 150, 8000.00, 'failed', 'RWF', '2026-09-05 10:20:00', 'Payment of 8000 RWF to Divine Store Ltd failed. Fee 150 RWF. TxId: FTX10023460');

-- ============================
-- 4. System_Logs
-- (transaction_id 1-5 references Transactions inserted above)
-- ============================
INSERT INTO System_Logs (transaction_id, process_stage, log_message, log_status) VALUES
(1, 'Completed', 'Transaction parsed, categorized, and loaded successfully', 'Success'),
(2, 'Completed', 'Airtime transaction processed without issues', 'Success'),
(3, 'Completed', 'Bill payment matched and loaded into database', 'Success'),
(4, 'Processing', 'Withdrawal transaction awaiting agent confirmation', 'Info'),
(5, 'Validated', 'Merchant payment failed validation - insufficient funds flagged', 'Error');

-- ============================
-- 5. Transaction_participants
-- Each transaction needs one sender + one receiver row
-- (Userid 1-5 references Users inserted above; Transactionid 1-5 references Transactions)
-- ============================
INSERT INTO Transaction_participants (Userid, Transactionid, role) VALUES
(1, 1, 'sender'),
(2, 1, 'receiver'),
(2, 2, 'sender'),
(5, 2, 'receiver'),
(3, 3, 'sender'),
(5, 3, 'receiver'),
(4, 4, 'sender'),
(5, 4, 'receiver'),
(1, 5, 'sender'),
(5, 5, 'receiver');

-- ============================
-- UPDATE TEST
-- Scenario: The pending withdrawal (Transaction_id 4) gets confirmed/completed
-- ============================

-- Before: check current state
SELECT Transaction_id, Status, Amount FROM Transactions WHERE Transaction_id = 4;

-- Run the update
UPDATE Transactions
SET Status = 'Completed'
WHERE Transaction_id = 4;

-- After: confirm it changed
SELECT Transaction_id, Status, Amount FROM Transactions WHERE Transaction_id = 4;

-- Also worth updating the related log to keep data consistent
UPDATE System_Logs
SET process_stage = 'Completed', log_message = 'Withdrawal confirmed by agent and completed', log_status = 'Success'
WHERE transaction_id = 4;

SELECT * FROM System_Logs WHERE transaction_id = 4;


-- ============================
-- DELETE TEST
-- Scenario: Remove a single test log entry (log_id 5, the error log for the failed transaction)
-- ============================

-- Before: confirm it exists
SELECT * FROM System_Logs WHERE log_id = 5;

-- Run the delete
DELETE FROM System_Logs WHERE log_id = 5;

-- After: confirm it's gone
SELECT * FROM System_Logs WHERE log_id = 5;
-- (should return 0 rows)
