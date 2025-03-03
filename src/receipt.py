from .baseimage import BaseImage
from .dataprovider import DataProvider
from .barcode_handler import BarcodeHandler
from .elements import ReceiptElements


class Receipt(BaseImage, DataProvider, BarcodeHandler, ReceiptElements):
    """Main Receipt class that inherits from all the base classes"""
    def __init__(
        self,
        mode: str = "L",
        size: tuple = (448, 888),
        color: tuple = (255, ),
        lang: str = "hebrew"
    ):
        # Initialize all parent classes
        BaseImage.__init__(self, mode, size, color, lang, "rtl")
        DataProvider.__init__(self, lang)
        # No need to explicitly initialize BarcodeHandler and ReceiptElements 
        # as they don't have __init__ methods
        
        # Any Receipt-specific initialization
        self.total_without_maam = 0.0