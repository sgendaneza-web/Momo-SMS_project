
EXPLAIN SELECT * FROM Users WHERE account_type = 'agent';

EXPLAIN SELECT * FROM Transactions
WHERE Transaction_date BETWEEN '2026-09-01' AND '2026-09-05';

EXPLAIN SELECT * FROM Transactions WHERE Status = 'Pending';
-- Expect: key = idx_transactions_status

EXPLAIN SELECT * FROM Transactions WHERE Financial_Transaction_id = 'FTX10023458';
EXPLAIN SELECT * FROM System_Logs WHERE log_status = 'Error';

EXPLAIN SELECT * FROM Transaction_participants WHERE Userid = 5;

SHOW INDEX FROM Users;
SHOW INDEX FROM Categories;
SHOW INDEX FROM Transactions;
SHOW INDEX FROM System_Logs;
SHOW INDEX FROM Transaction_participants;