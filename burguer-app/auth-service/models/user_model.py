"""
Este módulo contém a função de serialização para o modelo de usuário.
"""

def serialize_user(user):

    """Serializa um objeto de usuário em um dicionário.

    Returns:
        dict: Dicionário contendo os dados do usuário.
    """
    return {
        "email": user.get("email"),
        "name": user.get("name", ""),
        "address": user.get("address", ""),
        "role": user.get("role", "cliente")
    }
