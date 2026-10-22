from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    """Jeton du lien d'activation.

    Il contient l'état « actif » du compte : une fois le compte activé,
    le même lien ne fonctionne plus (lien à usage unique).
    """

    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_active}"


generatorToken = TokenGenerator()
