import os
import cv2
from datetime import datetime

def rename(filename):
    timestamp = datetime.timestamp(datetime.now())
    pieces = filename.split(".")
    return ".".join(pieces[:-1]) + str(int(timestamp)) + "." + pieces[-1]


def transform(
    model,
    img_name="input.jpg",
    delete_input=False,
):
    try:
        img_in_path = os.path.join('./images', img_name)
        img_out_path = os.path.join('./output', img_name)
        img_in = cv2.imread(img_in_path)
        img_out = model.predict(img_in)

        if not os.path.exists('./output'):
            os.mkdir('./output')

        cv2.imwrite(img_out_path, img_out)

    except Exception as error:
        print(error)
        res = "-1"

    else:
        res = img_out_path

    finally:
        try:
            if delete_input:
                os.remove(img_in_path)
        except Exception as error:
            print(error)
        finally:
            return res
