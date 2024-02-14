import requests

def saveImg(url, name):
    # 发送 GET 请求获取图片数据
    response = requests.get(url)

    # 检查响应状态码
    if response.status_code == 200:
        # 将图片内容保存到本地文件
        with open('assets/' + name, 'wb') as f:
            f.write(response.content)
    else:
        print("图片下载失败！")

# saveImg('https://image.gamersky.com/webimg13/db/palworld_wiki/pet/Sparkit.webp')
