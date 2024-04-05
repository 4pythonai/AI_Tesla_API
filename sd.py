import requests
import io
import base64
from PIL import Image


def sd_image(prompt):

    ## 8 卡机器 内网 IP
    url = "http://127.0.0.1:35600"

    # "prompt": "best quality, ultra-detailed, masterpiece, finely detail, highres, 8k wallpaper, (a single car of  1Tesla  model3 :1.3), solo,side view, (motion:1.5) ",

    payload = {
        "prompt": prompt,
        "steps": 30,
        "width": 1024,
        "batch_size": 1,
        "n_iter": 4,
        "height": 1024,
    }

    # 设置 模型
    opt = requests.get(url=f"{url}/sdapi/v1/options", timeout=30)
    opt_json = opt.json()
    # print(opt_json)
    opt_json["sd_model_checkpoint"] = "sd_xl_base_1.0.safetensors [31e35c80fc]"
    requests.post(url=f"{url}/sdapi/v1/options", json=opt_json, timeout=30)

    # 开始绘图
    print("开始绘图.....")
    response = requests.post(
        url=f"{url}/sdapi/v1/txt2img", json=payload, timeout=30, stream=True
    )
    print("Request Done.....")
    r = response.json()
    print("解码返回的图片.....")

    idx = 0
    for i in r["images"]:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))
        fname = "images/output" + str(idx) + ".png"
        print("保存" + fname)
        image.save(fname)
        idx = idx + 1
    print("绘图结束....")
