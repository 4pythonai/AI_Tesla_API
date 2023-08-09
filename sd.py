import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin

# url = "https://34d559366475b7f6e6.gradio.live"
url ="http://119.254.88.180:7860"

payload = {
     "prompt": "2girls",
     "steps": 30,
     "width": 1024, 
     "batch_size": 1,
     "n_iter": 2, 
     "height": 1024
}


# 设置 模型
opt = requests.get(url=f'{url}/sdapi/v1/options')
opt_json = opt.json()
# print(opt_json)
opt_json['sd_model_checkpoint'] = 'sd_xl_base_1.0.safetensors [31e35c80fc]'
requests.post(url=f'{url}/sdapi/v1/options', json=opt_json)


# 开始绘图
response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
print("Message get")
print(response.text)


r = response.json()
idx =0
for i in r['images']:
    image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
    fname="output" +str(idx)+".png"
    image.save(fname)
    idx= idx +1
