ALTER TABLE accounts
ADD COLUMN IF NOT EXISTS email TEXT;

-- Make it unique (allows multiple NULLs until you make it NOT NULL)
CREATE UNIQUE INDEX IF NOT EXISTS accounts_email_unique
ON accounts (lower(email))
WHERE email IS NOT NULL;

