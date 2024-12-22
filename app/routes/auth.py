from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("auth", __name__, url_prefix="/auth")

# Ruta de registro
@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Verifica que las contraseñas coincidan
        if password != confirm_password:
            flash("Las contraseñas no coinciden.", "error")
            return redirect(url_for("auth.register"))

        # Cifra la contraseña
        hashed_password = generate_password_hash(password)

        # Guardar en la base de datos (lógica que implementaremos más adelante)
        # Por ejemplo: save_user_to_db(name, phone, email, hashed_password)

        flash("Usuario registrado con éxito.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


# Ruta de inicio de sesión
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Busca el usuario en la base de datos (lógica que implementaremos más adelante)
        # Por ejemplo: user = get_user_by_email(email)

        user = None  # Esto se reemplazará con la consulta a la base de datos
        if not user or not check_password_hash(user.password, password):
            flash("Credenciales inválidas. Por favor, intente nuevamente.", "error")
            return redirect(url_for("auth.login"))

        # Inicia sesión
        session["user_id"] = user.id
        flash("Inicio de sesión exitoso.", "success")
        return redirect(url_for("document.documents"))

    return render_template("login.html")


# Ruta de cierre de sesión
@bp.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for("auth.login"))
