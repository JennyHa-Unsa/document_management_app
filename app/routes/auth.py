from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import pyotp
from twilio.rest import Client
from app.services.user_functions import get_user_by_email, get_user_by_id, save_user_to_db


bp = Blueprint("auth", __name__, url_prefix="/auth")

# Configuración de Twilio
TWILIO_ACCOUNT_SID = "tu_account_sid"
TWILIO_AUTH_TOKEN = "tu_auth_token"
TWILIO_PHONE_NUMBER = "+1234567890"  # Número de Twilio

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

        try:
            save_user_to_db(name, phone, email, password)
            flash("Usuario registrado con éxito.", "success")
            return redirect(url_for("auth.login"))
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for("auth.register"))

    return render_template("register.html")


# Ruta de inicio de sesión (Paso 1)
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Busca el usuario en la base de datos
        user = get_user_by_email(email)
        if not user or not check_password_hash(user.password_hash, password):
            flash("Credenciales inválidas. Por favor, intente nuevamente.", "error")
            return redirect(url_for("auth.login"))

        # Genera un código OTP y envía por SMS
        totp = pyotp.TOTP(user.otp_secret)
        otp_code = totp.now()
        send_otp_via_sms(user.phone, otp_code)

        # Guarda el estado temporal en la sesión
        session["temp_user_id"] = user.id_usuario
        flash("Se ha enviado un código OTP a tu número de teléfono.", "info")
        return redirect(url_for("auth.verify_otp"))

    return render_template("login.html")


# Ruta para verificar OTP (Paso 2)
@bp.route("/verify", methods=["GET", "POST"])
def verify_otp():
    if request.method == "POST":
        otp_code = request.form.get("otp_code")

        # Recupera el usuario temporal desde la sesión
        user_id = session.get("temp_user_id")
        if not user_id:
            flash("Error en la autenticación. Por favor, intente nuevamente.", "error")
            return redirect(url_for("auth.login"))

        # Busca al usuario en la base de datos
        user = get_user_by_id(user_id)
        totp = pyotp.TOTP(user.otp_secret)

        # Verifica el código OTP
        if not totp.verify(otp_code):
            flash("Código OTP inválido. Por favor, intente nuevamente.", "error")
            return redirect(url_for("auth.verify_otp"))

        # Autenticación completada
        session["user_id"] = user.id_usuario
        session.pop("temp_user_id", None)  # Limpia el estado temporal
        flash("Autenticación exitosa.", "success")
        return redirect(url_for("document.documents"))

    return render_template("verify.html")


# Ruta de cierre de sesión
@bp.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for("auth.login"))


# Función para enviar OTP por SMS
def send_otp_via_sms(phone, otp_code):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Tu código OTP es: {otp_code}",
        from_=TWILIO_PHONE_NUMBER,
        to=phone
    )
    print(f"Mensaje enviado: {message.sid}")
