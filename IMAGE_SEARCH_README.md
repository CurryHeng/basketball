# 球星图片搜索下载器

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `image_searcher.py` | Python版搜索下载脚本 |
| `image_search.html` | 网页版搜索界面 |

---

## 方法一：Python脚本版

### 1. 安装依赖

```bash
pip install requests
```

### 2. 运行脚本

```bash
python image_searcher.py
```

### 3. 选择模式

```
==================================================
🏀 球星图片搜索下载器
==================================================
✅ 图片保存目录: D:\...\images

📋 预设球星列表:
  1. stephen curry
  2. lebron james
  3. kevin durant
  ...

请选择模式:
  1. 搜索单个球星
  2. 批量下载所有预设球星
  3. 自定义搜索

请输入选项 (1/2/3): 
```

### 4. API Key配置（可选）

编辑 `image_searcher.py` 顶部的配置：

```python
API_KEYS = {
    'unsplash': '你的Unsplash Key',
    'pexels': '你的Pexels Key',
    'pixabay': '你的Pixabay Key',
}
```

**获取方式：**
- **Unsplash**: https://unsplash.com/developers → 注册 → 创建应用 → 获取 Access Key
- **Pexels**: https://www.pexels.com/api/ → 注册 → 获取 API Key
- **Pixabay**: https://pixabay.com/api/docs/ → 注册 → 获取 API Key

**注意：** 不配置API Key也可以使用，会使用Unsplash的随机图片接口。

---

## 方法二：网页版

### 1. 打开页面

直接双击 `image_search.html` 或用 Live Server 打开

### 2. 搜索图片

- 点击预设按钮（库里、詹姆斯等）
- 或输入自定义关键词搜索

### 3. 下载图片

- 点击单张图片的"下载此图"按钮
- 或点击"下载全部图片"

**注意：** 网页版下载有浏览器安全限制，部分图片可能需要右键另存为。

---

## 📥 下载结果示例

```
📥 开始批量下载 5 张图片...
  📥 下载中: stephen_curry_unsplash_abc123.jpg
  ✅ 下载成功: stephen_curry_unsplash_abc123.jpg (156.3 KB)
     保存路径: D:\code\codearts\baskertball\images\stephen_curry_unsplash_abc123.jpg
  📥 下载中: stephen_curry_unsplash_def456.jpg
  ✅ 下载成功: stephen_curry_unsplash_def456.jpg (203.7 KB)
     保存路径: D:\code\codearts\baskertball\images\stephen_curry_unsplash_def456.jpg
...

✅ 成功下载: 5/5 张
```

---

## 🔧 功能特点

### Python版
- ✅ 支持多API源（Unsplash、Pexels、Pixabay）
- ✅ 自动创建目标目录
- ✅ 完善的异常处理
- ✅ 10秒请求超时
- ✅ 详细的下载日志
- ✅ 批量下载支持

### 网页版
- ✅ 可视化界面
- ✅ 预设球星快捷按钮
- ✅ 图片预览
- ✅ 单张/批量下载
- ✅ 下载日志显示

---

## ⚠️ 常见问题

### Q: Python版提示"请求超时"？
A: 检查网络连接，或尝试使用代理

### Q: 网页版下载失败？
A: 浏览器安全限制，请右键图片选择"另存为"

### Q: 图片质量不理想？
A: 配置API Key后可获得更精准的搜索结果

### Q: 下载的图片在哪里？
A: Python版保存在 `./images/` 目录

---

## 🎯 使用场景

1. **球星资料库**：下载球员头像
2. **天赋分析**：获取示例图片
3. **演示展示**：快速获取配图
4. **素材收集**：批量下载主题图片
