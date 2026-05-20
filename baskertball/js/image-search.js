/**
 * 球星图片搜索 - 前端版本
 * 使用免费图片API，无需后端服务器
 */

class ImageSearcher {
    constructor() {
        this.unsplashKey = localStorage.getItem('unsplash_key') || '';
        this.pexelsKey = localStorage.getItem('pexels_key') || '';
        this.currentImages = [];
        this.selectedImages = new Set();
        
        this.init();
    }
    
    init() {
        // 加载保存的API Key
        if (this.unsplashKey) {
            document.getElementById('unsplash-key').value = this.unsplashKey;
        }
        if (this.pexelsKey) {
            document.getElementById('pexels-key').value = this.pexelsKey;
        }
        
        this.bindEvents();
    }
    
    bindEvents() {
        // 保存配置
        document.getElementById('save-config').addEventListener('click', () => {
            this.saveConfig();
        });
        
        // 预设按钮
        document.querySelectorAll('.preset-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                document.getElementById('search-input').value = btn.dataset.query;
                this.search(btn.dataset.query);
            });
        });
        
        // 搜索按钮
        document.getElementById('search-btn').addEventListener('click', () => {
            const query = document.getElementById('search-input').value.trim();
            if (query) this.search(query);
        });
        
        // 回车搜索
        document.getElementById('search-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const query = e.target.value.trim();
                if (query) this.search(query);
            }
        });
        
        // 下载全部
        document.getElementById('download-all-btn').addEventListener('click', () => {
            this.downloadAll();
        });
    }
    
    saveConfig() {
        this.unsplashKey = document.getElementById('unsplash-key').value.trim();
        this.pexelsKey = document.getElementById('pexels-key').value.trim();
        
        localStorage.setItem('unsplash_key', this.unsplashKey);
        localStorage.setItem('pexels_key', this.pexelsKey);
        
        alert('✅ 配置已保存！');
    }
    
    async search(query) {
        const source = document.getElementById('source-select').value;
        const statusEl = document.getElementById('status');
        const searchBtn = document.getElementById('search-btn');
        
        statusEl.textContent = '🔍 搜索中...';
        searchBtn.disabled = true;
        document.getElementById('images-grid').innerHTML = '';
        this.currentImages = [];
        this.selectedImages.clear();
        
        try {
            let images = [];
            
            if (source === 'unsplash') {
                images = await this.searchUnsplash(query);
            } else if (source === 'pexels') {
                images = await this.searchPexels(query);
            }
            
            this.currentImages = images;
            
            if (images.length === 0) {
                statusEl.textContent = '❌ 未找到图片';
                return;
            }
            
            statusEl.textContent = `✅ 找到 ${images.length} 张图片`;
            this.renderImages(images);
            document.getElementById('actions-bar').classList.remove('hidden');
            
        } catch (error) {
            statusEl.textContent = `❌ 搜索失败: ${error.message}`;
        } finally {
            searchBtn.disabled = false;
        }
    }
    
    async searchUnsplash(query) {
        const count = 12;
        
        // 如果有API Key，使用官方API
        if (this.unsplashKey) {
            try {
                const url = `https://api.unsplash.com/search/photos?query=${encodeURIComponent(query)}&per_page=${count}`;
                const response = await fetch(url, {
                    headers: { 'Authorization': `Client-ID ${this.unsplashKey}` }
                });
                
                if (!response.ok) throw new Error('API请求失败');
                
                const data = await response.json();
                
                return data.results.map(item => ({
                    id: item.id,
                    url: item.urls.regular,
                    downloadUrl: item.urls.full,
                    thumbnail: item.urls.thumb,
                    description: item.description || item.alt_description || query,
                    source: 'Unsplash',
                    author: item.user.name,
                    link: item.links.html
                }));
            } catch (e) {
                console.warn('Unsplash API失败，使用备用方案', e);
            }
        }
        
        // 无API Key或失败，使用Source API
        const images = [];
        for (let i = 0; i < count; i++) {
            const sig = Date.now() + i;
            images.push({
                id: `unsplash_${sig}`,
                url: `https://source.unsplash.com/400x400/?${encodeURIComponent(query)}&sig=${sig}`,
                downloadUrl: `https://source.unsplash.com/600x600/?${encodeURIComponent(query)}&sig=${sig}`,
                thumbnail: `https://source.unsplash.com/100x100/?${encodeURIComponent(query)}&sig=${sig}`,
                description: `${query} - 图片 ${i + 1}`,
                source: 'Unsplash',
                author: 'Unsplash',
                link: 'https://unsplash.com'
            });
        }
        return images;
    }
    
    async searchPexels(query) {
        if (!this.pexelsKey) {
            alert('请先配置 Pexels API Key');
            return [];
        }
        
        try {
            const url = `https://api.pexels.com/v1/search?query=${encodeURIComponent(query)}&per_page=12`;
            const response = await fetch(url, {
                headers: { 'Authorization': this.pexelsKey }
            });
            
            if (!response.ok) throw new Error('API请求失败');
            
            const data = await response.json();
            
            return data.photos.map(item => ({
                id: item.id,
                url: item.src.large,
                downloadUrl: item.src.original,
                thumbnail: item.src.tiny,
                description: item.alt || query,
                source: 'Pexels',
                author: item.photographer,
                link: item.url
            }));
        } catch (e) {
            throw new Error('Pexels API失败: ' + e.message);
        }
    }
    
    renderImages(images) {
        const grid = document.getElementById('images-grid');
        
        grid.innerHTML = images.map((img, index) => `
            <div class="image-card" data-index="${index}">
                <div class="image-wrapper">
                    <div class="image-loading">加载中...</div>
                    <img src="${img.url}" 
                         alt="${img.description}" 
                         loading="lazy"
                         onload="this.previousElementSibling.style.display='none'"
                         onerror="this.previousElementSibling.textContent='加载失败'">
                    <div class="image-overlay">
                        <span class="overlay-text">点击查看大图</span>
                    </div>
                </div>
                <div class="image-info">
                    <div class="image-desc">${img.description}</div>
                    <div class="image-meta">
                        <span class="image-source">${img.source} · ${img.author}</span>
                        <button class="download-btn" data-index="${index}">下载</button>
                    </div>
                </div>
            </div>
        `).join('');
        
        // 绑定下载按钮
        grid.querySelectorAll('.download-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const index = parseInt(btn.dataset.index);
                this.downloadSingle(this.currentImages[index]);
            });
        });
        
        // 绑定卡片点击（查看大图）
        grid.querySelectorAll('.image-card').forEach(card => {
            card.addEventListener('click', () => {
                const index = parseInt(card.dataset.index);
                const img = this.currentImages[index];
                window.open(img.downloadUrl || img.url, '_blank');
            });
        });
    }
    
    async downloadSingle(image) {
        this.addLog(`📥 开始下载: ${image.description}`, '');
        
        try {
            // 方法1: fetch + blob
            const response = await fetch(image.downloadUrl || image.url);
            const blob = await response.blob();
            
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${image.source}_${image.id}.jpg`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            this.addLog(`✅ 下载成功: ${image.source}_${image.id}.jpg`, 'success');
            
        } catch (error) {
            // 方法2: 直接打开
            this.addLog(`⚠️ 自动下载失败，已打开新窗口`, '');
            window.open(image.downloadUrl || image.url, '_blank');
        }
    }
    
    async downloadAll() {
        const images = this.currentImages;
        
        this.addLog(`📥 开始批量下载 ${images.length} 张图片...`, '');
        
        for (let i = 0; i < images.length; i++) {
            await this.downloadSingle(images[i]);
            await new Promise(resolve => setTimeout(resolve, 300));
        }
        
        this.addLog(`🎉 批量下载完成！`, 'success');
    }
    
    addLog(message, type = '') {
        const logContent = document.getElementById('log-content');
        const log = document.getElementById('download-log');
        
        const item = document.createElement('div');
        item.className = `log-item ${type ? 'log-' + type : ''}`;
        
        const time = new Date().toLocaleTimeString();
        item.textContent = `[${time}] ${message}`;
        
        logContent.appendChild(item);
        log.classList.remove('hidden');
        
        // 自动滚动到底部
        logContent.scrollTop = logContent.scrollHeight;
    }
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    new ImageSearcher();
});
