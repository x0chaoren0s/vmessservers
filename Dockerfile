# 使用官方Python镜像作为基础镜像
FROM python:3.9.19-alpine3.20

# 下面是一些创建者的基本信息
LABEL author=x0chaoren0s
LABEL email=xxy.hubery@foxmail.com
LABEL version='0.4'

# 安装git
# RUN apk add --no-cache git

# 设置工作目录
WORKDIR /app

# 将当前目录下的文件拷贝到工作目录
COPY . /app

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# yesCaptcha的key
ENV API_KEY "ddd1cf72d9955a0e8ca7d05597fea5eb1dce33de5331"
ENV MODE "RELEASE"

# 启动应用
CMD ["python", "run.py"]