"""
donations.py

Donation/order utilities for the Food Donations app.

A donation is treated as an order.
Status values:
- pending
- completed
"""

import os
from typing import List, Dict, Any, Optional

import psycopg
from psycopg.rows import dict_row

from database.accounts import verify_login, get_account_id_by_name

DEFAULT_DSN = os.getenv("DATABASE_URL", "postgresql://localhost:5432/food_donations")


def get_conn():
    return psycopg.connect(DEFAULT_DSN, row_factory=dict_row)


def create_donation(account_id: int, notes: Optional[str] = None) -> int:
    """
    Creates a new donation/order with status='pending' by default.
    Returns the donation id.
    """
    sql = """
    INSERT INTO donations (account_id, notes, status)
    VALUES (%(account_id)s, %(notes)s, 'pending')
    RETURNING id;
    """

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, {
                "account_id": account_id,
                "notes": notes,
            })
            row = cur.fetchone()
            return int(row["id"])


def create_donation_by_login(account_name: str, password: str, notes: Optional[str] = None) -> int:
    """
    Creates a donation/order for a user identified by account_name + password.
    """
    if not verify_login(account_name, password):
        raise ValueError("Invalid account name or password")

    account_id = get_account_id_by_name(account_name)
    if account_id is None:
        raise ValueError("Account not found")

    return create_donation(account_id, notes)


def add_donation_item(
    donation_id: int,
    food_name: str,
    quantity: Optional[float] = None,
    unit: Optional[str] = None,
    category: Optional[str] = None,
) -> int:
    """
    Adds one food item to a donation.
    Returns the donation_item id.
    """
    sql = """
    INSERT INTO donation_items (donation_id, food_name, quantity, unit, category)
    VALUES (%(donation_id)s, %(food_name)s, %(quantity)s, %(unit)s, %(category)s)
    RETURNING id;
    """

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, {
                "donation_id": donation_id,
                "food_name": food_name.strip(),
                "quantity": quantity,
                "unit": unit.strip() if isinstance(unit, str) and unit.strip() else None,
                "category": category.strip() if isinstance(category, str) and category.strip() else None,
            })
            row = cur.fetchone()
            return int(row["id"])


def list_donations_for_account(account_name: str, password: str) -> List[Dict[str, Any]]:
    """
    Lists all donations/orders for a given account, newest first.
    """
    if not verify_login(account_name, password):
        raise ValueError("Invalid account name or password")

    account_id = get_account_id_by_name(account_name)
    if account_id is None:
        raise ValueError("Account not found")

    sql = """
    SELECT id, account_id, donated_at, notes, status
    FROM donations
    WHERE account_id = %(account_id)s
    ORDER BY donated_at DESC;
    """

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, {"account_id": account_id})
            return [dict(row) for row in cur.fetchall()]


def list_pending_orders() -> List[Dict[str, Any]]:
    """
    Returns all pending orders with their account addresses.
    Does NOT modify them.
    """
    sql = """
    SELECT
        d.id AS donation_id,
        a.account_name,
        a.address_line1,
        a.address_line2,
        a.city,
        a.state,
        a.postal_code,
        d.donated_at,
        d.notes,
        d.status
    FROM donations d
    JOIN accounts a ON a.id = d.account_id
    WHERE d.status = 'pending'
    ORDER BY d.donated_at ASC;
    """

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            return [dict(row) for row in cur.fetchall()]


def fulfill_pending_orders() -> List[Dict[str, Any]]:
    """
    Returns all pending order addresses and marks those orders as completed
    in the same transaction.
    """
    sql = """
    WITH updated AS (
        UPDATE donations d
        SET status = 'completed'
        WHERE d.status = 'pending'
        RETURNING d.id, d.account_id, d.donated_at, d.notes, d.status
    )
    SELECT
        u.id AS donation_id,
        a.account_name,
        a.address_line1,
        a.address_line2,
        a.city,
        a.state,
        a.postal_code,
        u.donated_at,
        u.notes,
        u.status
    FROM updated u
    JOIN accounts a ON a.id = u.account_id
    ORDER BY u.donated_at ASC;
    """

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            return [dict(row) for row in cur.fetchall()]


if __name__ == "__main__":
    print("donations.py ready")
