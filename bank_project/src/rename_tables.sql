-- Rename user-related tables
ALTER TABLE accounts_user RENAME TO users_user;
ALTER TABLE accounts_user_groups RENAME TO users_user_groups;
ALTER TABLE accounts_user_user_permissions RENAME TO users_user_user_permissions;
ALTER TABLE accounts_user_favorite_users RENAME TO users_user_favorite_users;

-- Rename transaction-related tables
ALTER TABLE transfer_reasons RENAME TO transactions_transfer_reasons;
ALTER TABLE transactions RENAME TO transactions_transactions;
