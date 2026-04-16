-- Add email column if missing
ALTER TABLE accounts
ADD COLUMN IF NOT EXISTS email TEXT;

CREATE UNIQUE INDEX IF NOT EXISTS accounts_email_unique
ON accounts (lower(email))
WHERE email IS NOT NULL;

-- Add status column to donations if missing
ALTER TABLE donations
ADD COLUMN IF NOT EXISTS status TEXT NOT NULL DEFAULT 'pending';

ALTER TABLE donations
DROP CONSTRAINT IF EXISTS donations_status_check;

ALTER TABLE donations
ADD CONSTRAINT donations_status_check
CHECK (status IN ('pending', 'completed'));

CREATE INDEX IF NOT EXISTS donations_status_idx
ON donations(status);

-- Account reset codes table
CREATE TABLE IF NOT EXISTS account_codes (
  id           BIGSERIAL PRIMARY KEY,
  email        TEXT NOT NULL,
  purpose      TEXT NOT NULL,
  code_hash    TEXT NOT NULL,
  expires_at   TIMESTAMPTZ NOT NULL,
  used_at      TIMESTAMPTZ,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS account_codes_email_purpose_idx
ON account_codes (lower(email), purpose);

CREATE INDEX IF NOT EXISTS account_codes_expires_idx
ON account_codes (expires_at);
