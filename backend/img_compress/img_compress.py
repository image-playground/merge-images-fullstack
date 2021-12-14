from PIL import Image
import io
import math

# 微信公众号限制图片大小于10Mb
DEFAULT_MAX_IMG_SIZE = 10 * 1024 * 1024 * 0.9
# 微信公众号限制长宽乘积小于600万
DEFAULT_MAX_IMG_DIMENSION = 6000000
DEFAULT_SCALE = 0.9


def _compress_img_by_pct(img: Image.Image, pct: float) -> Image.Image:
    w, h = img.size
    w = int(w * pct)
    h = int(h * pct)
    return img.resize((w, h), Image.ANTIALIAS)


def compress_img(
    img: Image.Image,
    max_img_size: float = DEFAULT_MAX_IMG_SIZE,
    scale: float = DEFAULT_SCALE
) -> Image.Image:
    assert 0 < scale < 1
    format = img.format
    while True:
        w, h = img.size
        if w * h > DEFAULT_MAX_IMG_DIMENSION:
            pct = math.sqrt(DEFAULT_MAX_IMG_DIMENSION / w / h)
            img = _compress_img_by_pct(img, pct)
            w, h = img.size
        with io.BytesIO() as bytes:
            # 存储在内存中时必须指定文件格式
            img.save(bytes, format=format)
            bytes_size = bytes.tell()
            print(
                f"bytes size: {bytes_size:10}, img size: {img.size}, pixels: {w*h/10000}w")
            if bytes_size > max_img_size:
                pct = math.sqrt(max_img_size / bytes_size)
                pct = min(pct, scale)
                img = _compress_img_by_pct(img, pct)
            else:
                break
    return img


if __name__ == "__main__":
    import os
    choice = 0
    if choice == 1:
        img_path = "/Users/mark/Projects/merge_imgs/backend/output/人生是一场永不落幕的演出.png"
        img_name = os.path.basename(img_path)
        print(f"img_name: {img_name}")
        img = Image.open(img_path)
        compressed_img = compress_img(img)
        compressed_img.save(img_name)
    elif choice == 0:
        dir_path = "/Users/mark/Projects/merge_imgs/backend/output"
        for img_name in os.listdir(dir_path):
            if img_name.endswith("png"):
                print(f"handling img: {img_name}")
                img_path = os.path.join(dir_path, img_name)
                img_size = os.stat(img_path).st_size
                compress_img(Image.open(img_path)).save(img_path)
