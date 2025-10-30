"""Serialização para retorno (removendo dados sensíveis)"""


def serialize_user(user):
    """Serializa os dados do usuário para retorno.
    Args:
        user (dict): Usuário a ser serializado

    Returns:
        dict: Dicionário com os dados do usuário serializados
    """
    return {
        "email": user.get("email"),
        "name": user.get("name"),
        "address": user.get("address"),
        "role": user.get("role", "cliente"),
    }
