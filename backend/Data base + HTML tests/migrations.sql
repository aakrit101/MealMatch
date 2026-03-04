-- Add email column if missing
ALTER TABLE accounts
ADD COLUMN IF NOT EXISTS email TEXT;

CREATE UNIQUE INDEX IF NOT EXISTS accounts_email_unique
ON accounts (lower(email))
WHERE email IS NOT NULL;


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



