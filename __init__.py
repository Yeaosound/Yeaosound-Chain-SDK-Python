from ysc_tools import ysc
import configloader
__all__ = ["ysc","setconfig"]
def setconfig(**kargs):
    c = configloader.config()
    for key in kargs:
        c.setkey(key,kargs[key])
    c.save()