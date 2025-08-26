from libqtile.log_utils import logger


logger.warning("your message")


try:
    from libqtile.widget import PulseVolume

    PulseVolume()

except Exception:
    logger.exception("Oh oh")
