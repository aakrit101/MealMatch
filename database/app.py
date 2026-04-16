from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.exceptions import BadRequest

from dotenv import load_dotenv
load_dotenv()


from accounts import (
    create_account,
    verify_login,
    list_accounts,
    update_account_by_login,
    delete_account_by_login,
    request_code,
    lookup_username_by_email,
    reset_password_by_email,
)

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"  # needed for flash messages


# ---------- Helpers ----------
def cleaned(form, name: str):
    v = (form.get(name) or "").strip()
    return v if v else None


# ---------- Pages ----------
@app.get("/")
def home():
    return render_template("home.html")


@app.get("/accounts")
def list_accounts_page():
    accounts = list_accounts()
    return render_template("list_accounts.html", accounts=accounts)


@app.get("/accounts/new")
def new_account_page():
    return render_template("create_account.html")


@app.get("/accounts/edit")
def edit_account_page():
    return render_template("update_account.html")


@app.get("/accounts/remove")
def delete_account_page():
    return render_template("delete_account.html")


@app.get("/login")
def login_page():
    return render_template("login.html")


@app.get("/forgot-username")
def forgot_username_page():
    return render_template("forgot_username.html")


@app.get("/forgot-username/verify")
def forgot_username_verify_page():
    email = (request.args.get("email") or "").strip().lower()
    return render_template("forgot_username_verify.html", email=email)


@app.get("/forgot-password")
def forgot_password_page():
    return render_template("forgot_password.html")


@app.get("/reset-password")
def reset_password_page():
    email = (request.args.get("email") or "").strip().lower()
    return render_template("reset_password.html", email=email)


# ---------- Form handlers ----------
@app.post("/accounts/create")
def create_account_handler():
    try:
        account_id = create_account(
            account_name=request.form["account_name"].strip(),
            password=request.form["password"],
            email=request.form["email"].strip(),
            address_line1=request.form["address_line1"].strip(),
            address_line2=(request.form.get("address_line2") or "").strip() or None,
            city=request.form["city"].strip(),
            state=request.form["state"].strip(),
            postal_code=request.form["postal_code"].strip(),
            food_genre=request.form["food_genre"].strip(),
        )
    except KeyError as e:
        raise BadRequest(f"Missing field: {e}")

    flash(f"Account created! New account id: {account_id}", "success")
    return redirect(url_for("home"))


@app.post("/accounts/update")
def update_account_handler():
    account_name = cleaned(request.form, "account_name")
    password = request.form.get("password") or ""

    if not account_name or not password:
        flash("Account name and password are required.", "error")
        return redirect(url_for("edit_account_page"))

    try:
        updated = update_account_by_login(
            account_name=account_name,
            password=password,
            new_account_name=cleaned(request.form, "new_account_name"),
            new_password=cleaned(request.form, "new_password"),
            email=cleaned(request.form, "email"),
            address_line1=cleaned(request.form, "address_line1"),
            address_line2=cleaned(request.form, "address_line2"),
            city=cleaned(request.form, "city"),
            state=cleaned(request.form, "state"),
            postal_code=cleaned(request.form, "postal_code"),
            food_genre=cleaned(request.form, "food_genre"),
        )
    except ValueError as e:
        flash(str(e), "error")
        return redirect(url_for("edit_account_page"))

    flash(f"Account updated: {updated['account_name']}", "success")
    return redirect(url_for("home"))


@app.post("/accounts/delete")
def delete_account_handler():
    account_name = (request.form.get("account_name") or "").strip()
    password = request.form.get("password") or ""

    if not account_name or not password:
        flash("Account name and password are required.", "error")
        return redirect(url_for("delete_account_page"))

    try:
        delete_account_by_login(account_name, password)
    except ValueError as e:
        flash(str(e), "error")
        return redirect(url_for("delete_account_page"))

    flash(f"Account deleted: {account_name}", "success")
    return redirect(url_for("home"))


@app.post("/login")
def login_handler():
    account_name = (request.form.get("account_name") or "").strip()
    password = request.form.get("password") or ""

    if not account_name or not password:
        flash("Missing account name or password.", "error")
        return redirect(url_for("login_page"))

    ok = verify_login(account_name, password)
    if ok:
        flash("Login successful!", "success")
        return redirect(url_for("home"))
    else:
        flash("Invalid login.", "error")
        return redirect(url_for("login_page"))


# ----- Forgot username -----
@app.post("/forgot-username")
def forgot_username_send_code():
    email = (request.form.get("email") or "").strip().lower()
    if not email:
        flash("Email is required.", "error")
        return redirect(url_for("forgot_username_page"))

    code = request_code(email, "forgot_username", minutes_valid=10)
    print(f"[DEV] Forgot-username code for {email}: {code}")  # prints to terminal

    flash("A code was generated (check the server terminal). Enter it below.", "success")
    return redirect(url_for("forgot_username_verify_page", email=email))


@app.post("/forgot-username/verify")
def forgot_username_verify():
    email = (request.form.get("email") or "").strip().lower()
    code = (request.form.get("code") or "").strip()

    username = lookup_username_by_email(email, code)
    if not username:
        flash("Invalid or expired code.", "error")
        return redirect(url_for("forgot_username_verify_page", email=email))

    flash(f"Your account name is: {username}", "success")
    return redirect(url_for("login_page"))


# ----- Forgot / Reset password -----
@app.post("/forgot-password")
def forgot_password_send_code():
    email = (request.form.get("email") or "").strip().lower()
    if not email:
        flash("Email is required.", "error")
        return redirect(url_for("forgot_password_page"))

    code = request_code(email, "reset_password", minutes_valid=10)
    print(f"[DEV] Password reset code for {email}: {code}")  # prints to terminal

    flash("A reset code was generated (check the server terminal). Enter it below.", "success")
    return redirect(url_for("reset_password_page", email=email))


@app.post("/reset-password")
def reset_password_handler():
    email = (request.form.get("email") or "").strip().lower()
    code = (request.form.get("code") or "").strip()
    new_password = request.form.get("new_password") or ""

    if not email or not code or not new_password:
        flash("Email, code, and new password are required.", "error")
        return redirect(url_for("reset_password_page", email=email))

    ok = reset_password_by_email(email, code, new_password)
    if not ok:
        flash("Invalid or expired code.", "error")
        return redirect(url_for("reset_password_page", email=email))

    flash("Password reset successful. Please log in.", "success")
    return redirect(url_for("login_page"))


if __name__ == "__main__":
    # http://127.0.0.1:5000
    app.run(debug=True)
