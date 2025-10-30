"""User Service para operações relacionadas a usuários"""

from config.database import get_db
from models.user_model import serialize_user
from werkzeug.security import generate_password_hash

db = get_db()
users_col = db["users"]


def create_user(email, password, name, address, role="cliente"):
    """Cria um novo usuário.

    Args:
        email (string): Endereço de e-mail do usuário. Deve ser único no sistema.
        password (string): Senha do usuário
        name (string): Nome do usuário
        address (string): Endereço do usuário
        role (str, optional): Função do usuário. Defaults to "cliente".

    Returns:
        tuple: Mensagem de sucesso ou erro e o status HTTP correspondente
    """
    # Verifica se email já existe
    if users_col.find_one({"email": email}):
        return {"error": "Usuário já existe"}, 400

    hashed_pw = generate_password_hash(password)
    user = {
        "email": email,
        "password": hashed_pw,
        "name": name,
        "address": address,
        "role": role,
    }
    users_col.insert_one(user)
    return {"message": "Usuário criado com sucesso"}, 201


def get_user_by_email(email):
    """Obtém um usuário pelo e-mail.

    Args:
        email (string): Endereço de e-mail do usuário.

    Returns:
        string: Dados do usuário ou None se não encontrado.
    """
    user = users_col.find_one({"email": email})
    if user:
        return serialize_user(user)
    return None


def update_user(email, name, address):
    """Atualiza um usuŕio pelo email

    Args:
        email (string): Email do usuário a ser atualizado.
        name (string): Nome do usuário a ser atualizado.
        address (string): Endereço do usuário a ser atualizado.
    """
    users_col.update_one({"email": email}, {"$set": {"name": name, "address": address}})


def delete_user(email):
    """Delete um usuário pelo email

    Args:
        email (string): Email do usuário a ser deletado.
    """
    users_col.delete_one({"email": email})
