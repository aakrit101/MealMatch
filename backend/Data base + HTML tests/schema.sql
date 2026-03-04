CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE accounts (
  id              BIGSERIAL PRIMARY KEY,
  account_name    TEXT NOT NULL UNIQUE,
  email TEXT NOT NULL UNIQUE,
  password_hash   TEXT NOT NULL,
  address_line1   TEXT NOT NULL,
  address_line2   TEXT,
  city            TEXT NOT NULL,
  state           TEXT NOT NULL,
  postal_code     TEXT NOT NULL,
  food_genre      TEXT NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE donations (
  id           BIGSERIAL PRIMARY KEY,
  account_id   BIGINT NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
  donated_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
  notes        TEXT
);

CREATE TABLE donation_items (
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
  purpose      TEXT NOT NULL,  -- 'forgot_username' or 'reset_password'
  code_hash    TEXT NOT NULL,
  expires_at   TIMESTAMPTZ NOT NULL,
  used_at      TIMESTAMPTZ,

  created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS account_codes_email_purpose_idx
ON account_codes (lower(email), purpose);

CREATE INDEX IF NOT EXISTS account_codes_expires_idx
ON account_codes (expires_at);
