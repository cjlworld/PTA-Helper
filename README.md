# PTA-Helper

PTA-Helper 是一个浏览器插件，调用 LLM 接口进行 PTA 答案解析。

## 使用方式

您需要使用 Chrome 或者 Edge 浏览器才能使用该插件。

这里以 Edge 为例。

```
git clone https://github.com/cjlworld/PTA-Helper.git
```

打开 Edge 开发者模式 并 打开扩展页面，将 extension 文件夹拖入该页面即可完成安装。

## 部署方式

首先将 `backend/config.yaml` 中的 API key 替换为您的 API key，将项目 clone 到本地。 

```shell
git clone https://github.com/cjlworld/PTA-Helper.git
cd PTA-Helper/backend
```

### 方案一 Python

您可以使用 `python -m venv venv` 创建一个虚拟环境并激活，然后执行

```shell
pip install -r requirements.txt
python app.py
```

### 方案二 Docker

需要 docker 环境。

```shell
docker build -t pta_helper .
docker run -d -p 18080:18080 --name pta_helper pta_helper
```

***

部署完成后修改 `extension/content.js` 中的 `BASE_URL` 为您部署的后端地址即可。

 ```js
 const BASE_URL = "https://...";
 ```

