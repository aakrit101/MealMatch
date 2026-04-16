CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS accounts (
  id              BIGSERIAL PRIMARY KEY,
  account_name    TEXT NOT NULL UNIQUE,
  password_hash   TEXT NOT NULL,
  email           TEXT,
  address_line1   TEXT NOT NULL,
  address_line2   TEXT,
  city            TEXT NOT NULL,
  state           TEXT NOT NULL,
  postal_code     TEXT NOT NULL,
  food_genre      TEXT NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS accounts_email_unique
ON accounts (lower(email))
WHERE email IS NOT NULL;

CREATE TABLE IF NOT EXISTS donations (
  id           BIGSERIAL PRIMARY KEY,
  account_id   BIGINT NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
  donated_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
  notes        TEXT,
  status       TEXT NOT NULL DEFAULT 'pending',
  CONSTRAINT donations_status_check CHECK (status IN ('pending', 'completed'))
);

CREATE TABLE IF NOT EXISTS donation_items (
  id            BIGSERIAL PRIMARY KEY,
  donation_id   BIGINT NOT NULL REFERENCES donations(id) ON DELETE CASCADE,
  food_name     TEXT NOT NULL,
  quantity      NUMERIC(12,2),
  unit          TEXT,
  category      TEXT
);

CREATE TABLE IF NOT EXISTS account_codes (
  id           BIGSERIAL PRIMARY KEY,
  email        TEXT NOT NULL,
  purpose      TEXT NOT NULL,
  code_hash    TEXT NOT NULL,
  expires_at   TIMESTAMPTZ NOT NULL,
  used_at      TIMESTAMPTZ,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS donations_account_id_idx
ON donations(account_id);

CREATE INDEX IF NOT EXISTS donations_status_idx
ON donations(status);

CREATE INDEX IF NOT EXISTS donation_items_donation_id_idx
ON donation_items(donation_id);

CREATE INDEX IF NOT EXISTS account_codes_email_purpose_idx
ON account_codes (lower(email), purpose);

CREATE INDEX IF NOT EXISTS account_codes_expires_idx
ON account_codes (expires_at);
