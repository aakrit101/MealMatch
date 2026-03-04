"""
accounts.py

PostgreSQL-backed account utilities for the Food Donations app.

Python version: 3.9+ (uses Optional[...] not PEP604 unions)

Requires Postgres extension:
  CREATE EXTENSION IF NOT EXISTS pgcrypto;

Environment:
  export DATABASE_URL="postgresql://user:pass@localhost:5432/food_donations"
or defaults to:
  postgresql://localhost:5432/food_donations
"""

import os
import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, List

import psycopg
from psycopg.rows import dict_row


# --- Connection ---
DEFAULT_DSN = os.getenv("DATABASE_URL", "postgresql://localhost:5432/food_donations")


def get_conn():
    # autocommit False so we can rollback on errors automatically on context exit
    return psycopg.connect(DEFAULT_DSN, row_factory=dict_row)


# ----------------------------
# Accounts: Create / Read / Update / Delete
# ----------------------------

def create_account(
    account_name: str,
    password: str,
    email: str,
    address_line1: str,
    city: str,
    state: str,
    postal_code: str,
    food_genre: str,
    address_line2: Optional[str] = None,
) -> int:
    """
    Creates an account and returns the new account id.
    Password is hashed using pgcrypto: crypt(password, gen_salt('bf')).
    Email is stored lowercased.
    """
    sql = """
    INSERT INTO accounts (
      account_name, password_hash, email,
      address_line1, address_line2, city, state, postal_code,
      food_genre
    )
    VALUES (
      %(account_name)s,
      crypt(%(password)s, gen_salt('bf')),
      %(email)s,
      %(address_line1)s, %(address_line2)s, %(city)s, %(state)s, %(postal_code)s,
      %(food_genre)s
    )
    RETURNING id;
    """

    params = {
        "account_name": account_name.strip(),
        "password": password,
        "email": email.strip().lower(),
        "address_line1": address_line1.strip(),
        "address_line2": address_line2.strip() if isinstance(address_line2, str) and address_line2.strip() else None,
        "city": city.strip(),
        "state": state.strip(),
        "postal_code": postal_code.strip(),
        "food_genre": food_genre.strip(),
    }

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            row = cur.fetchone()
            return int(row["id"])


def list_accounts() -> List[dict]:
    """
    Returns a list of accounts (safe fields only; no password_hash).
    """
    sql = """
    SELECT id, account_name, email,
           address_line1, address_line2, city, state, postal_code,
           food_genre, created_at
    FROM accounts
    ORDER BY created_at DESC;
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            return [dict(r) for r in cur.fetchall()]


def get_account_id_by_name(account_name: str) -> Optional[int]:
    sql = "SELECT id FROM accounts WHERE account_name = %(account_name)s;"
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, {"account_name": account_name.strip()})
            row = cur.fetchone()
            return int(row["id"]) if row else None


def get_account_id_by_email(email: str) -> Optional[int]:
    sql = "SELECT id FROM accounts WHERE lower(email) = lower(%(email)s);"
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, {"email": email.strip().lower()})
            row = cur.fetchone()
            return int(row["id"]) if row else None


def verify_login(account_name: str, password: str) -> bool:
    """
    Returns True if password matches for that account_name.
    """
    sql = """
    SELECT (password_hash = crypt(%(password)s, password_hash)) AS ok
    FROM accounts
    WHERE account_name = %(account_name)s;
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, {"account_name": account_name.strip(), "password": password})
            row = cur.fetchone()
            return bool(row and row["ok"])


def delete_account(account_id: int) -> None:
    """
    Deletes the account. Because schema uses ON DELETE CASCADE,
    it will also delete that account’s donations + donation_items.
    """
    sql = "DELETE FROM accounts WHERE id = %(id)s;"
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, {"id": account_id})


def update_account(
    account_id: int,
    *,
    account_name: Optional[str] = None,
    new_password: Optional[str] = None,
    email: Optional[str] = None,
    address_line1: Optional[str] = None,
    address_line2: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    postal_code: Optional[str] = None,
    food_genre: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Updates any provided fields (leave as None to keep existing).
    Returns the updated account row as a dict (includes email but not password_hash).
    """
    set_clauses = []
    params: Dict[str, Any] = {"id": account_id}

    if account_name is not None:
        set_clauses.append("account_name = %(account_name)s")
        params["account_name"] = account_name.strip()

    if new_password is not None:
        set_clauses.append("password_hash = crypt(%(new_password)s, gen_salt('bf'))")
        params["new_password"] = new_password

    if email is not None:
        set_clauses.append("email = %(email)s")
        params["email"] = email.strip().lower()

    if address_line1 is not None:
        set_clauses.append("address_line1 = %(address_line1)s")
        params["address_line1"] = address_line1.strip()

    if address_line2 is not None:
        set_clauses.append("address_line2 = %(address_line2)s")
        params["address_line2"] = address_line2.strip() if address_line2.strip() else None

    if city is not None:
        set_clauses.append("city = %(city)s")
        params["city"] = city.strip()

    if state is not None:
        set_clauses.append("state = %(state)s")
        params["state"] = state.strip()

    if postal_code is not None:
        set_clauses.append("postal_code = %(postal_code)s")
        params["postal_code"] = postal_code.strip()

    if food_genre is not None:
        set_clauses.append("food_genre = %(food_genre)s")
        params["food_genre"] = food_genre.strip()

    if not set_clauses:
        sql = """
        SELECT id, account_name, email,
               address_line1, address_line2, city, state, postal_code,
               food_genre, created_at
        FROM accounts
        WHERE id = %(id)s;
        """
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, {"id": account_id})
                row = cur.fetchone()
                if row is None:
                    raise ValueError("Account not found")
                return dict(row)

    sql = f"""
    UPDATE accounts
    SET {", ".join(set_clauses)}
    WHERE id = %(id)s
    RETURNING id, account_name, email,
              address_line1, address_line2, city, state, postal_code,
              food_genre, created_at;
    """

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            row = cur.fetchone()
            if row is None:
                raise ValueError("Account not found")
            return dict(row)


def update_account_by_login(
    account_name: str,
    password: str,
    *,
    new_account_name: Optional[str] = None,
    new_password: Optional[str] = None,
    email: Optional[str] = None,
    address_line1: Optional[str] = None,
    address_line2: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    postal_code: Optional[str] = None,
    food_genre: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Update an account using login credentials instead of id.
    """
    if not verify_login(account_name, password):
        raise ValueError("Invalid account name or password")

    account_id = get_account_id_by_name(account_name)
    if account_id is None:
        raise ValueError("Account not found")

    return update_account(
        account_id,
        account_name=new_account_name,
        new_password=new_password,
        email=email,
        address_line1=address_line1,
        address_line2=address_line2,
        city=city,
        state=state,
        postal_code=postal_code,
        food_genre=food_genre,
    )


def delete_account_by_login(account_name: str, password: str) -> None:
    """
    Delete an account using login credentials instead of id.
    """
    if not verify_login(account_name, password):
        raise ValueError("Invalid account name or password")

    account_id = get_account_id_by_name(account_name)
    if account_id is None:
        raise ValueError("Account not found")

    delete_account(account_id)


# ----------------------------
# Dev-mode code flows (no email yet)
# ----------------------------

def _hash_code(code: str) -> str:
    # store only a hash of the code in DB (never the raw code)
    return hashlib.sha256(code.encode("utf-8")).hexdigest()


def request_code(email: str, purpose: str, minutes_valid: int = 10) -> str:
    """
    Creates a one-time code, stores its hash with expiry, and returns the raw code.
    Caller (Flask) should print the raw code to terminal in dev mode.

    purpose: 'forgot_username' or 'reset_password'
    """
    email = email.strip().lower()
    code = f"{secrets.randbelow(1_000_000):06d}"  # 6-digit code
    code_hash = _hash_code(code)
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=minutes_valid)

    sql = """
    INSERT INTO account_codes (email, purpose, code_hash, expires_at)
    VALUES (%(email)s, %(purpose)s, %(code_hash)s, %(expires_at)s);
    """

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, {
                "email": email,
                "purpose": purpose,
                "code_hash": code_hash,
                "expires_at": expires_at,
            })

    return code


def _consume_code(email: str, purpose: str, code: str) -> bool:
    """
    Validates a code and marks it used. Returns True if valid+consumed.
    """
    email = email.strip().lower()
    code_hash = _hash_code(code.strip())

    sql = """
    UPDATE account_codes
    SET used_at = now()
    WHERE id = (
      SELECT id
      FROM account_codes
      WHERE lower(email) = lower(%(email)s)
        AND purpose = %(purpose)s
        AND code_hash = %(code_hash)s
        AND used_at IS NULL
        AND expires_at > now()
      ORDER BY created_at DESC
      LIMIT 1
    )
    RETURNING id;
    """

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, {"email": email, "purpose": purpose, "code_hash": code_hash})
            row = cur.fetchone()
            return bool(row)


def lookup_username_by_email(email: str, code: str) -> Optional[str]:
    """
    'Forgot username' flow: verify code then return account_name.
    """
    if not _consume_code(email, "forgot_username", code):
        return None

    sql = "SELECT account_name FROM accounts WHERE lower(email) = lower(%(email)s);"
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, {"email": email.strip().lower()})
            row = cur.fetchone()
            return row["account_name"] if row else None


def reset_password_by_email(email: str, code: str, new_password: str) -> bool:
    """
    'Reset password' flow: verify code then update password_hash.
    Returns True on success.
    """
    if not _consume_code(email, "reset_password", code):
        return False

    sql = """
    UPDATE accounts
    SET password_hash = crypt(%(new_password)s, gen_salt('bf'))
    WHERE lower(email) = lower(%(email)s)
    RETURNING id;
    """

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, {"email": email.strip().lower(), "new_password": new_password})
            row = cur.fetchone()
            return bool(row)


if __name__ == "__main__":
    # Tiny manual test (adjust values)
    # NOTE: requires accounts.email column and account_codes table in DB
    print("Connected to:", DEFAULT_DSN)
