from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    """
    Checkout name and handle the ready function
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "checkout"

    def ready(self):
        import checkout.signals
