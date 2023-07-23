"""
Гененрирует QR коды
"""
from io import BytesIO
from pathlib import Path

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask, RadialGradiantColorMask
from qrcode.image.styles.moduledrawers.pil import CircleModuleDrawer

current_dir = Path(__file__).resolve().parent

class QrCodeGenerator:

    def generate(self, data: str):
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
        qr.add_data(data)
        embeded_image_path = current_dir / 'logo.png'
        self.img = qr.make_image(image_factory=StyledPilImage,
                                 module_drawer=CircleModuleDrawer(),
                                 color_mask=RadialGradiantColorMask(),
                                 embeded_image_path=str(embeded_image_path),
                                 )

    def save(self, stream: BytesIO = None):
        if stream is None:
            with open("test_image.png", "wb") as file:
                self.img.save(file)
        else:
            self.img.save(stream)


if __name__ == '__main__':
    generator = QrCodeGenerator()
    generator.generate(data='dafdsalkjsadlnkgfajkg')
    from io import BytesIO
    file = BytesIO()
    generator.save(stream=file)
    file.seek(0)
    print(file.read()[:100])
