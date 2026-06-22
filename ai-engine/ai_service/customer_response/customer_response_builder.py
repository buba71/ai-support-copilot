class CustomerResponseBuilder:
    def build_from_analysis(self, analysis: dict) -> str:
        if analysis.get("insufficient_context"):
            return (
                "Bonjour,\n\n"
                "Merci pour votre message. "
                "Nous avons bien reçu votre demande, mais les informations disponibles "
                "ne permettent pas encore d’apporter une réponse définitive. "
                "Votre dossier va être vérifié par un conseiller afin de vous apporter "
                "une réponse adaptée.\n\n"
                "Cordialement,\n"
                "Le service client"
            )

        if analysis.get("escalation_required"):
            return (
                "Bonjour,\n\n"
                "Merci pour votre message. "
                "Votre demande nécessite une vérification approfondie par notre équipe support. "
                "Nous allons transmettre votre dossier à un conseiller spécialisé afin de vous "
                "apporter une réponse adaptée.\n\n"
                "Cordialement,\n"
                "Le service client"
            )

        return (
            "Bonjour,\n\n"
            "Merci pour votre message. "
            "Après analyse de votre demande, notre équipe a identifié la procédure applicable. "
            "Nous allons traiter votre dossier conformément à notre politique support.\n\n"
            "Cordialement,\n"
            "Le service client"
        )