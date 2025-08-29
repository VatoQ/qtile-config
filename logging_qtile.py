from libqtile.log_utils import logger


logger.warning("your message")


try:
    from qtile_extras import widget

    widget.GlobalMenu(
            background="#111111"
            )

    logger.warning("No error occured")
except Exception:
    logger.exception("Oh oh")
