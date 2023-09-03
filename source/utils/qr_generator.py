import qrcode
from qrcode.main import QRCode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SquareGradiantColorMask
from io import BytesIO


def create_qr_code_from_config_as_link_str(config: str) -> BytesIO:
    """creates qr code from peer data

    Args:
        config (str): peer data (config file), which will be encoded in qr code

    Returns:
        BytesIO: qr code image
    """
    qr: QRCode = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )

    qr.add_data(config)
    qr.make(fit=True)

    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=SquareGradiantColorMask(
            center_color=(220, 0, 220), edge_color=(0, 0, 64)
        ),
        embeded_image_path="source/data/logo_circle.png",
    )

    img_io = BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)
    return img_io


if __name__ == "__main__":
    peer_data = "vless://4c3fe585-ac09-41df-b284-70d3fbe18884@62.84.103.109:443?security=reality&fp=chrome&pbk=PGeJ1HmM32wOc-1316onHLdHqbr5ISte9PKB_xBmX3g&sid=9887c63522d89153&type=tcp&flow=xtls-rprx-vision&encryption=none#TR_FAMILY_"
    img_io = create_qr_code_from_config_as_link_str(peer_data)

    with open("qr_code.png", "wb") as f:
        f.write(img_io.read())
