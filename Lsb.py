from skimage import io
import re


def encode(s):
    value = ''
    for c in s:
        o = ord(c)
        t = bin(o)
        t = t.replace('0b', '')
        t = ''.join([i for i in ['0'] * (16 - len(t))]) + t
        value = value + t
    return value


def decode(s):
    l = re.findall(r'.{16}', s)
    s = ''
    for i in l:
        s = s + chr(int(i, 2))
    return s


def hide():
    path = input('请输入图片路径(如D:/1.jpg):')
    path = path.replace("\\", "/")
    img = io.imread(path)
    width, height, c = img.shape
    print("此图片可以隐藏:", width * height // 16, "个字符")
    message = input("请输入要隐藏的信息:")
    length = len(message)
    binLength = bin(length).replace('0b', '')
    binLength = ''.join(['0'] * (16 - len(binLength))) + binLength
    binMsg = encode(message)
    binMsg = binLength + binMsg
    total = len(binMsg)
    index = 0
    for i in range(width):
        for j in range(height):
            img[i, j, 0] = img[i, j, 0] & 254
            img[i, j, 0] = img[i, j, 0] + int(binMsg[index])
            index += 1
            if index >= total:
                break
        if index >= total:
            break
    fname = input("请输入保存路径，不带文件扩展名，如D:/pic ,将保存为D:/pic.png\n")
    io.imsave(fname + ".png", img)  # 这里用jpg数据会出错，其他格式没试过
    print("图片已保存为" + fname + ".png")


def display():
    path = input('请输入含有信息的图片路径:')
    path = path.replace("\\", "/")
    img = io.imread(path)
    width, height, c = img.shape
    num = ''
    index = 0
    for i in range(width):
        for j in range(height):
            num = num + str(img[i, j, 0] & 1)
            index += 1
            if index == 16:
                break
        if index == 16:
            break
    num = int(num, 2) + 1  # 数据空间 +长度空间
    total = num * 16
    binMsg = ''
    index = 0
    print("解析中，请等待...")
    for i in range(width):
        for j in range(height):
            binMsg = binMsg + str(img[i, j, 0] & 1)
            index += 1
            if index > total:
                break
        if index > total:
            break
    message = decode(binMsg[16:])
    print("message=", message)


if __name__ == '__main__':
    while True:
        op = input("1.隐藏信息到图片\n2.从图片中读取信息\n3.退出\n")
        if op == "1":
            hide()
        elif op == "2":
            display()
        elif op == "3":
            break
        else:
            print("请输入正确的选项")
