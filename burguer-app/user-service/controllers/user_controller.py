"""User Controller for handling user-related routes"""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from services.user_service import (
    create_user,
    delete_user,
    get_user_by_email,
    update_user,
)

user_bp = Blueprint("user", __name__)


@user_bp.route("/create", methods=["GET", "POST"])
def create():
    """Rota de criação de usuário

    Returns:
        render_template: Renderiza o template de criação de usuário ou redireciona após criação bem-sucedida.
    """
    if request.method == "POST":
        data = request.form
        response, status = create_user(
            email=data["email"],
            password=data["password"],
            name=data["name"],
            address=data["address"],
            role=data.get("role", "cliente"),
        )
        if status != 201:
            flash(response["error"])
            return redirect(url_for("user.create"))
        flash("Usuário criado com sucesso! Faça login para continuar.")
        # Redirect to auth-service login after successful registration
        return redirect("http://localhost:5000/auth/login")
    return render_template("create.html")


@user_bp.route("/profile/<email>")
def profile(email):
    """Rota para exibir o perfil de um usuário.

    Args:
        email (string): Email do usuário

    Returns:
        render_template: Renderiza o template de perfil do usuário ou retorna erro se não encontrado.
    """
    user = get_user_by_email(email)
    if not user:
        return "Usuário não encontrado", 404
    return render_template("profile.html", user=user)


@user_bp.route("/edit/<email>", methods=["GET", "POST"])
def edit(email):
    """Rota para editar o perfil de um usuário.
    Args:
        email (string): Email do usuário
    Returns:
        render_template: Renderiza o template de edição do usuário ou redireciona após atualização
    """
    user = get_user_by_email(email)
    if request.method == "POST":
        name = request.form["name"]
        address = request.form["address"]
        update_user(email, name, address)
        flash("Perfil atualizado com sucesso.")
        return redirect(url_for("user.profile", email=email))
    return render_template("edit.html", user=user)


@user_bp.route("/delete/<email>", methods=["POST"])
def delete(email):
    """Rota para remover um usário

    Args:
        email (string): Email do usuário a ser excluído.

    Returns:
        redirect: Redireciona para a rota de criação de usuário após exclusão.
    """
    delete_user(email)
    flash("Usuário excluído com sucesso.")
    return redirect(url_for("user.create"))
