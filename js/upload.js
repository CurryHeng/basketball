// 球迷分享画廊模块
const FanGallery = {
  _currentPlayerId: null,
  _pendingFile: null,
  _lightboxImages: [],
  _lightboxIndex: 0,

  ALLOWED_TYPES: ["image/jpeg", "image/png", "image/gif", "image/webp"],
  MAX_SIZE: 5 * 1024 * 1024,

  init(playerId) {
    this._currentPlayerId = playerId;
    this._pendingFile = null;
    this._lightboxImages = [];
    this._lightboxIndex = 0;

    // 恢复缓存的昵称
    const savedName = localStorage.getItem("bb_upload_nickname") || "";
    const nameInput = document.getElementById("upload-nickname");
    if (nameInput) nameInput.value = savedName;

    this._resetForm();
    this._bindEvents();
    this._bindLightboxKeyboard();
    this._loadGallery();
  },

  _bindEvents() {
    const zone = document.getElementById("upload-zone");
    const fileInput = document.getElementById("upload-file-input");
    const selectBtn = document.getElementById("upload-select-btn");
    const submitBtn = document.getElementById("upload-submit-btn");
    const nameInput = document.getElementById("upload-nickname");

    // 拖拽事件
    if (zone) {
      zone.addEventListener("dragover", (e) => {
        e.preventDefault();
        zone.classList.add("drag-over");
      });
      zone.addEventListener("dragleave", () => zone.classList.remove("drag-over"));
      zone.addEventListener("drop", (e) => {
        e.preventDefault();
        zone.classList.remove("drag-over");
        if (e.dataTransfer.files.length > 0) this._handleFiles(e.dataTransfer.files);
      });
    }

    // 文件选择
    if (selectBtn && fileInput) {
      selectBtn.onclick = () => fileInput.click();
      fileInput.onchange = () => {
        if (fileInput.files.length > 0) this._handleFiles(fileInput.files);
        fileInput.value = "";
      };
    }

    // 上传按钮
    if (submitBtn) submitBtn.onclick = () => this._submitUpload();

    // 昵称自动保存
    if (nameInput) {
      nameInput.addEventListener("change", () => {
        localStorage.setItem("bb_upload_nickname", nameInput.value.trim());
      });
    }
  },

  _resetForm() {
    this._pendingFile = null;
    const preview = document.getElementById("upload-preview");
    const submitBtn = document.getElementById("upload-submit-btn");
    const status = document.getElementById("upload-status");
    if (preview) preview.classList.add("hidden");
    if (submitBtn) submitBtn.disabled = true;
    if (status) { status.textContent = ""; status.className = "upload-status"; }
  },

  _handleFiles(files) {
    const file = files[0];
    if (!file) return;

    // 验证类型
    if (!this.ALLOWED_TYPES.includes(file.type)) {
      this._showStatus("不支持的文件类型，仅支持 JPG/PNG/GIF/WebP", "error");
      return;
    }
    // 验证大小
    if (file.size > this.MAX_SIZE) {
      this._showStatus("文件过大，最大支持 5MB", "error");
      return;
    }

    this._pendingFile = file;
    this._showPreview(file);
  },

  _showPreview(file) {
    const preview = document.getElementById("upload-preview");
    const submitBtn = document.getElementById("upload-submit-btn");
    const status = document.getElementById("upload-status");
    if (status) { status.textContent = ""; status.className = "upload-status"; }

    if (!preview) return;
    preview.classList.remove("hidden");

    const url = URL.createObjectURL(file);
    preview.innerHTML = `
      <img class="upload-preview-thumb" src="${url}" alt="preview">
      <div class="upload-preview-info">
        <div class="upload-preview-name">${file.name}</div>
        <div class="upload-preview-size">${(file.size / 1024).toFixed(1)} KB</div>
      </div>
    `;

    if (submitBtn) submitBtn.disabled = false;
  },

  _showStatus(msg, type) {
    const el = document.getElementById("upload-status");
    if (!el) return;
    el.textContent = msg;
    el.className = "upload-status upload-status-" + type;
  },

  async _submitUpload() {
    if (!this._pendingFile || !this._currentPlayerId) return;

    const submitBtn = document.getElementById("upload-submit-btn");
    const nameInput = document.getElementById("upload-nickname");
    const uploaderName = nameInput ? nameInput.value.trim().slice(0, 20) : "";

    if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = "上传中..."; }

    // 保存昵称
    localStorage.setItem("bb_upload_nickname", uploaderName);

    const formData = new FormData();
    formData.append("file", this._pendingFile);
    formData.append("playerId", String(this._currentPlayerId));
    formData.append("uploaderName", uploaderName);

    try {
      const resp = await fetch(API_BASE + "/api/upload/upload", {
        method: "POST",
        body: formData,
      });
      const data = await resp.json();

      if (data.success) {
        this._showStatus("上传成功！", "success");
        this._resetForm();
        this._loadGallery();
      } else {
        this._showStatus(data.message || "上传失败", "error");
        if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = "上传"; }
      }
    } catch (e) {
      this._showStatus("连接失败，请检查网络或后端服务", "error");
      if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = "上传"; }
    }
  },

  async _loadGallery() {
    const grid = document.getElementById("gallery-grid");
    const empty = document.getElementById("gallery-empty");
    if (!grid) return;

    grid.innerHTML = "";

    try {
      const resp = await fetch(API_BASE + "/api/upload/list?playerId=" + this._currentPlayerId);
      const data = await resp.json();

      if (!data.success || !data.data || data.data.length === 0) {
        if (empty) empty.classList.remove("hidden");
        return;
      }

      if (empty) empty.classList.add("hidden");
      this._lightboxImages = data.data;
      this._renderGrid(data.data);

      // 绑定点击事件
      grid.querySelectorAll(".gallery-item").forEach((item) => {
        item.addEventListener("click", () => {
          const idx = parseInt(item.dataset.index);
          this._showLightbox(idx);
        });
      });
    } catch (e) {
      if (empty) empty.classList.remove("hidden");
    }
  },

  _renderGrid(uploads) {
    const grid = document.getElementById("gallery-grid");
    if (!grid) return;

    grid.innerHTML = uploads
      .map(
        (u, i) => `
      <div class="gallery-item" data-index="${i}">
        <img class="gallery-thumb"
             src="${this.getFileUrl(u.id)}"
             alt="${u.fileName}"
             loading="lazy"
             onerror="this.parentElement.style.display='none'">
        <div class="gallery-item-info">
          <span class="gallery-uploader">${this._esc(u.uploaderName)}</span>
          <span class="gallery-time">${this._formatTime(u.createdAt)}</span>
        </div>
      </div>`
      )
      .join("");
  },

  getFileUrl(id) {
    return API_BASE + "/api/upload/file?id=" + id;
  },

  // ====== Lightbox ======

  _bindLightboxKeyboard() {
    // 全局键盘事件，只绑定一次，通过检查 lightbox 是否可见来决定是否处理
    document.addEventListener("keydown", (e) => {
      const overlay = document.getElementById("lightbox-overlay");
      if (!overlay || overlay.classList.contains("hidden")) return;
      if (e.key === "Escape") this._closeLightbox();
      if (e.key === "ArrowLeft") this._navigate(-1);
      if (e.key === "ArrowRight") this._navigate(1);
    });

    const overlay = document.getElementById("lightbox-overlay");
    if (!overlay) return;

    // 关闭按钮
    const closeBtn = document.getElementById("lightbox-close");
    if (closeBtn) closeBtn.onclick = () => this._closeLightbox();

    // 点击背景关闭
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) this._closeLightbox();
    });

    // 导航按钮
    const prevBtn = document.getElementById("lightbox-prev");
    const nextBtn = document.getElementById("lightbox-next");
    if (prevBtn) prevBtn.onclick = () => this._navigate(-1);
    if (nextBtn) nextBtn.onclick = () => this._navigate(1);
  },

  _showLightbox(index) {
    if (!this._lightboxImages.length) return;
    this._lightboxIndex = index;

    const overlay = document.getElementById("lightbox-overlay");
    const img = document.getElementById("lightbox-image");
    const uploader = document.getElementById("lightbox-uploader");
    const time = document.getElementById("lightbox-time");
    const counter = document.getElementById("lightbox-counter");

    if (!overlay || !img) return;

    const rec = this._lightboxImages[index];
    img.src = this.getFileUrl(rec.id);
    img.alt = rec.fileName;
    if (uploader) uploader.textContent = rec.uploaderName;
    if (time) time.textContent = this._formatTime(rec.createdAt);
    if (counter) counter.textContent = `${index + 1} / ${this._lightboxImages.length}`;

    overlay.classList.remove("hidden");
    document.body.style.overflow = "hidden";
  },

  _navigate(delta) {
    const newIdx = this._lightboxIndex + delta;
    if (newIdx >= 0 && newIdx < this._lightboxImages.length) {
      this._showLightbox(newIdx);
    }
  },

  _closeLightbox() {
    const overlay = document.getElementById("lightbox-overlay");
    if (overlay) overlay.classList.add("hidden");
    document.body.style.overflow = "";
  },

  // ====== Helpers ======

  _esc(str) {
    const div = document.createElement("div");
    div.textContent = str || "anonymous";
    return div.innerHTML;
  },

  _formatTime(iso) {
    if (!iso) return "";
    const d = new Date(iso);
    const now = new Date();
    const diff = now - d;
    if (diff < 3600000) return Math.floor(diff / 60000) + "分钟前";
    if (diff < 86400000) return Math.floor(diff / 3600000) + "小时前";
    return d.toLocaleDateString("zh-CN");
  },
};
