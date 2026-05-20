// 认证模块 - 登录、注册、找回密码、修改昵称
// 后端 API 地址：本地开发默认为空（同源），部署时改为后端服务器地址
// 例如: const API_BASE = 'https://basketball-api.onrender.com';

const API_BASE = '';

const Auth = {
    _tokenKey: 'bb_auth_token',
    _userKey: 'bb_auth_user',

    getToken() {
        return localStorage.getItem(this._tokenKey);
    },

    getUser() {
        try {
            return JSON.parse(localStorage.getItem(this._userKey));
        } catch {
            return null;
        }
    },

    isLoggedIn() {
        return !!this.getToken();
    },

    _saveAuth(token, user) {
        localStorage.setItem(this._tokenKey, token);
        localStorage.setItem(this._userKey, JSON.stringify(user));
    },

    _clearAuth() {
        localStorage.removeItem(this._tokenKey);
        localStorage.removeItem(this._userKey);
    },

    async _post(path, body) {
        const headers = { 'Content-Type': 'application/json' };
        const token = this.getToken();
        if (token) {
            headers['Authorization'] = 'Bearer ' + token;
        }
        const resp = await fetch(path, {
            method: 'POST',
            headers,
            body: JSON.stringify(body)
        });
        return resp.json();
    },

    async _get(path) {
        const headers = {};
        const token = this.getToken();
        if (token) {
            headers['Authorization'] = 'Bearer ' + token;
        }
        const resp = await fetch(path, { headers });
        return resp.json();
    },

    async register(nickname, password, securityQuestion, securityAnswer) {
        const data = await this._post(API_BASE + '/api/auth/register', {
            nickname, password, securityQuestion, securityAnswer
        });
        if (data.success) {
            const loginData = await this.login(nickname, password);
            return loginData;
        }
        return data;
    },

    async login(nickname, password) {
        const data = await this._post(API_BASE + '/api/auth/login', { nickname, password });
        if (data.success) {
            this._saveAuth(data.token, data.user);
        }
        return data;
    },

    async logout() {
        const token = this.getToken();
        this._clearAuth();
        if (token) {
            await this._post(API_BASE + '/api/auth/logout', {});
        }
    },

    async getMe() {
        return this._get(API_BASE + '/api/auth/me');
    },

    async forgotPassword(nickname) {
        return this._post(API_BASE + '/api/auth/forgot-password', { nickname });
    },

    async verifyAnswer(nickname, securityAnswer) {
        return this._post(API_BASE + '/api/auth/verify-answer', { nickname, securityAnswer });
    },

    async resetPassword(nickname, resetToken, newPassword) {
        return this._post(API_BASE + '/api/auth/reset-password', { nickname, resetToken, newPassword });
    },

    async changeNickname(newNickname) {
        return this._post(API_BASE + '/api/auth/change-nickname', { newNickname });
    },

    async getSecurityQuestions() {
        const resp = await fetch(API_BASE + '/api/auth/security-questions');
        return resp.json();
    },

    updateNavUI() {
        const authBtn = document.getElementById('nav-auth-btn');
        if (!authBtn) return;

        if (this.isLoggedIn()) {
            const user = this.getUser();
            authBtn.innerHTML = '<span class="nav-user-info">' + (user ? user.nickname : '用户') + '</span>';
            authBtn.title = '点击退出登录';
            authBtn.classList.add('logged-in');
        } else {
            authBtn.innerHTML = '登录';
            authBtn.title = '登录 / 注册';
            authBtn.classList.remove('logged-in');
        }
    }
};
