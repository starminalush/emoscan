import io


def cnvt_image_to_bytes(image):
    image_byte_array = io.BytesIO()
    image.save(image_byte_array, format='JPEG')

    # Получите байты из байтового потока
    return image_byte_array.getvalue()
