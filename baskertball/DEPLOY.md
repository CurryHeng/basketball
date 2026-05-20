# 网页部署指南

## 🚀 快速部署

### 方式一：GitHub Pages（推荐，免费）

```bash
# 1. 创建 GitHub 仓库
# 2. 上传以下文件：
- index.html
- image-search.html
- css/style.css
- css/image-search.css
- js/main.js
- js/image-search.js
- data/players.json
- images/ (可选)
- gifs/ (可选)

# 3. 开启 GitHub Pages
仓库 Settings → Pages → Source: main branch → Save

# 4. 访问地址
https://你的用户名.github.io/仓库名/
```

### 方式二：Vercel（推荐，免费）

```bash
# 1. 安装 Vercel CLI
npm install -g vercel

# 2. 部署
vercel

# 3. 按提示操作，获得访问地址
```

### 方式三：Netlify（免费）

```bash
# 1. 访问 https://netlify.com
# 2. 拖拽整个项目文件夹到页面上传
# 3. 自动获得访问地址
```

---

## 📁 部署文件清单

### 必需文件（前端静态页面）

```
baskertball/
├── index.html              ✅ 球星资料库首页
├── image-search.html       ✅ 图片搜索页面
├── css/
│   ├── style.css          ✅ 主样式
│   └── image-search.css   ✅ 图片搜索样式
├── js/
│   ├── main.js            ✅ 主逻辑
│   └── image-search.js    ✅ 图片搜索逻辑
└── data/
    └── players.json       ✅ 球星数据
```

### 可选文件

```
├── images/                 # 球星头像（可选）
├── gifs/                   # 动作GIF（可选）
└── README.md              # 说明文档
```

---

## ⚠️ 重要：后端功能说明

### 需要后端的功能

| 功能 | 是否需要后端 | 替代方案 |
|------|-------------|----------|
| 球星资料展示 | ❌ 纯前端 | ✅ 使用本地JSON |
| 图片搜索下载 | ❌ 纯前端 | ✅ 直接调用图片API |
| 天赋分析 | ✅ 需要Flask | 见下方部署方案 |
| 排行榜 | ✅ 需要Flask | 见下方部署方案 |

---

## 🔧 后端部署方案（天赋分析功能）

### 方案一：Railway（推荐，免费额度）

```bash
# 1. 安装 Railway CLI
npm install -g @railway/cli

# 2. 登录
railway login

# 3. 创建项目
railway init

# 4. 部署
railway up

# 5. 设置环境变量
railway variables set UNSPLASH_KEY=你的key
```

### 方案二：Render（免费）

```bash
# 1. 访问 https://render.com
# 2. 创建 Web Service
# 3. 连接 GitHub 仓库
# 4. 设置：
- Build Command: pip install -r requirements.txt
- Start Command: python app.py
```

### 方案三：PythonAnywhere（免费）

```bash
# 1. 访问 https://pythonanywhere.com
# 2. 上传代码
# 3. 创建 Web App
# 4. 配置 WSGI
```

---

## 🌐 前后端分离部署

### 前端部署到 GitHub Pages

```
https://yourname.github.io/basketball/
```

### 后端部署到 Railway

```
https://your-app.railway.app
```

### 修改前端API地址

编辑 `js/main.js`：

```javascript
// 修改这行
const API_BASE = 'https://your-app.railway.app';
```

---

## 📝 部署检查清单

### 部署前检查

- [ ] 修改 `js/main.js` 中的 `API_BASE` 为后端地址
- [ ] 确认 `data/players.json` 存在
- [ ] 图片路径正确（本地图片或在线URL）
- [ ] API Key 已配置（存储在localStorage，不写代码里）

### 部署后测试

- [ ] 球星资料库正常显示
- [ ] 图片搜索功能正常
- [ ] 天赋分析能连接后端
- [ ] 排行榜能显示数据

---

## 🔒 安全提示

### API Key 管理

```javascript
// ❌ 错误：写在代码里
const API_KEY = 'abc123';

// ✅ 正确：让用户输入，存localStorage
localStorage.setItem('unsplash_key', userInput);
```

### 跨域配置

后端已配置 CORS，允许任意域名访问：

```python
CORS(app, resources={
    r"/api/*": {"origins": "*"}
})
```

---

## 💰 成本估算

| 平台 | 费用 | 限制 |
|------|------|------|
| GitHub Pages | 免费 | 静态站点 |
| Vercel | 免费 | 100GB带宽/月 |
| Netlify | 免费 | 100GB带宽/月 |
| Railway | 免费$5额度 | 500小时/月 |
| Render | 免费 | 750小时/月 |

---

## 📞 常见问题

### Q: 部署后图片不显示？
A: 检查图片路径，建议使用在线URL或确保图片一起部署

### Q: 天赋分析报错？
A: 确认后端已部署，修改前端的 `API_BASE` 地址

### Q: API Key 怎么配置？
A: 用户在网页上输入，存储在浏览器 localStorage

### Q: 后端启动失败？
A: 检查 `requirements.txt` 依赖是否安装
