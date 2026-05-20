# API Key 配置说明

## ⚠️ 重要：API Key 不能写在代码里！

请使用以下任一方式配置：

---

## 方式一：环境变量（推荐）

### Windows (PowerShell)
```powershell
$env:UNSPLASH_KEY = "你的unsplash_key"
$env:PEXELS_KEY = "你的pexels_key"
$env:PIXABAY_KEY = "你的pixabay_key"

# 然后运行
python image_searcher.py
```

### Windows (CMD)
```cmd
set UNSPLASH_KEY=你的unsplash_key
set PEXELS_KEY=你的pexels_key
set PIXABAY_KEY=你的pixabay_key

python image_searcher.py
```

### Linux / macOS
```bash
export UNSPLASH_KEY="你的unsplash_key"
export PEXELS_KEY="你的pexels_key"
export PIXABAY_KEY="你的pixabay_key"

python image_searcher.py
```

---

## 方式二：.env 文件（推荐）

### 1. 复制示例文件
```bash
复制 .env.example 为 .env
```

### 2. 编辑 .env 文件
```
# .env 文件内容

UNSPLASH_ACCESS_KEY=你的真实key
PEXELS_API_KEY=你的真实key
PIXABAY_API_KEY=你的真实key
```

### 3. 运行脚本
```bash
python image_searcher.py
```

---

## 方式三：config.ini 文件

### 1. 创建 config.ini 文件
```ini
[API]
unsplash = 你的unsplash_key
pexels = 你的pexels_key
pixabay = 你的pixabay_key
```

### 2. 运行脚本
```bash
python image_searcher.py
```

---

## 🔑 如何获取 API Key

### Unsplash（免费）
1. 访问 https://unsplash.com/developers
2. 注册账号
3. 创建新应用
4. 获取 **Access Key**

### Pexels（免费）
1. 访问 https://www.pexels.com/api/
2. 注册账号
3. 获取 **API Key**

### Pixabay（免费）
1. 访问 https://pixabay.com/api/docs/
2. 注册账号
3. 获取 **API Key**

---

## ✅ 不配置 API Key 也能用！

如果不配置任何 API Key，脚本会使用 **Unsplash Source API**（无需 Key 的免费接口），功能完全正常，只是搜索精度稍低。

---

## 🔒 安全提示

- ✅ `.env` 文件已添加到 `.gitignore`，不会被提交到 Git
- ✅ `config.ini` 也应该在 `.gitignore` 中
- ❌ 永远不要把 API Key 写在代码里
- ❌ 永远不要把 API Key 提交到公开仓库
