# 智扫通机器人智能客服

基于 LangChain ReAct Agent + RAG + Streamlit 的垂类扫地机器人智能客服系统。

## 项目简介

智扫通面向扫地机器人/扫拖一体机器人场景，使用 Agent + RAG 组合提供可检索、可追溯、可扩展的问答能力。

- RAG 增强检索：知识文档向量化后检索，降低幻觉。
- Tool Calling：可调用天气、定位、外部记录等工具。
- 动态提示词：根据上下文切换系统提示词。
- 流式输出：前端逐字显示，提升交互体验。
- MD5 去重入库：新增文档可增量入库，避免重复处理。

## 环境准备

1. Python 3.10+
2. 安装依赖

```bash
uv pip install -r requirements.txt
```

3. 配置环境变量（项目根目录复制 `.env.example` 为 `.env`）

```env
DASHSCOPE_API_KEY=你的DashScope密钥
GAODE_API_KEY=你的高德密钥
```

- DashScope 密钥可在 [DashScope 控制台](https://dashscope.console.aliyun.com/) 申请。
- 高德密钥也可临时写在 `config/agent.yml` 的 `gaodekey`，但更推荐放进 `.env` / Streamlit Secrets。

## 如何将新文件传入向量数据库

目前项目支持 `txt` 和 `pdf`，目录与格式配置在 `config/chroma.yml`：

- `data_path: data`
- `allow_knowledge_file_type: ["txt", "pdf"]`

最简单操作步骤：

1. 把新文档放到 `data/` 目录下（如 `data/产品手册.txt` 或 `data/说明书.pdf`）。
2. 运行入库命令：

```bash
uv run python -m rag.vector_store
```

说明：

- 项目会自动分片并写入 Chroma。
- 项目基于 `md5.text` 做去重，相同内容不会重复入库。

## 启动项目

```bash
streamlit run app.py
```

默认访问地址：`http://localhost:8501`

## 部署到 Streamlit Cloud（私有 GitHub）

让别人通过公网链接使用本应用：

1. 将本仓库推送到 **GitHub Private** 仓库（不要提交 `.env`）。
2. 打开 [Streamlit Community Cloud](https://share.streamlit.io/) ，用 GitHub 登录并授权访问私有仓库。
3. New app：
   - Repository：选择本仓库
   - Branch：`main`
   - Main file path：`app.py`
4. 在 App settings → **Secrets** 填入（TOML）：

```toml
DASHSCOPE_API_KEY = "你的DashScope密钥"
GAODE_API_KEY = "你的高德密钥"
```

5. Deploy 成功后，把 `https://xxx.streamlit.app` 链接发给他人即可。

说明：

- 仓库已包含 `chroma_db/`（约 3MB），云端可直接检索，无需重新入库。
- 若更新知识库：本地重新入库后提交 `chroma_db/` 与 `md5.text`，推送后 Cloud 会重新部署。

## 目录结构

```text
zhisaotong-Agent/
├── app.py
├── agent/
├── config/
├── data/
├── model/
├── rag/
├── utils/
├── chroma_db/
├── md5.text
├── .env.example
├── .streamlit/secrets.toml.example
└── requirements.txt
```
