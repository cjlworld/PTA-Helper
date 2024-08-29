# 使用官方 Python Alpine 基础镜像
FROM python:3.10-alpine

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 文件并安装依赖
COPY requirements.txt .

# 安装依赖并设置 pip 镜像源
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 复制应用程序代码
COPY . .

# 暴露端口
EXPOSE 18080

# 运行应用程序
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "18080"]