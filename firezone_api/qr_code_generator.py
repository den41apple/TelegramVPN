"""
Гененрирует QR коды
"""
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask, RadialGradiantColorMask
from qrcode.image.styles.moduledrawers.pil import CircleModuleDrawer
from typing.io import IO


class QrCodeGenerator:

    def generate(self, data: str):
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(data)
        self.img = qr.make_image(image_factory=StyledPilImage,
                                 module_drawer=CircleModuleDrawer(),
                                 color_mask=RadialGradiantColorMask(),
                                 embeded_image_path='logo.png',
                                 )

    def save(self, stream: IO = None):
        if stream is None:
            with open("test_image.png", "wb") as file:
                self.img.save(file)
        else:
            self.img.save(stream)


if __name__ == '__main__':
    generator = QrCodeGenerator()
    generator.generate()
    generator.save()
