let players = [];
let filteredPlayers = [];
let selectedTeam = '全部';
let searchQuery = '';
let debounceTimer = null;

const homePage = document.getElementById('home-page');
const detailPage = document.getElementById('detail-page');
const talentPage = document.getElementById('talent-page');
const rankingsPage = document.getElementById('rankings-page');
const authPage = document.getElementById('auth-page');
const userDetailPage = document.getElementById('user-detail-page');
const searchInput = document.getElementById('search-input');
const teamTagsContainer = document.getElementById('team-tags');
const cardsContainer = document.getElementById('cards-container');
const resultCount = document.getElementById('result-count');
const emptyState = document.getElementById('empty-state');
const clearFiltersBtn = document.getElementById('clear-filters');
const backBtn = document.getElementById('back-btn');

const navBtns = document.querySelectorAll('.nav-btn');
const talentForm = document.getElementById('talent-form');
const talentResult = document.getElementById('talent-result');
const rankingsList = document.getElementById('rankings-list');

navBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const page = btn.dataset.page;
        switchPage(page);
        navBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
    });
});

function switchPage(page) {
    homePage.classList.add('hidden');
    detailPage.classList.add('hidden');
    talentPage.classList.add('hidden');
    rankingsPage.classList.add('hidden');
    authPage.classList.add('hidden');
    userDetailPage.classList.add('hidden');

    if (page === 'home') {
        homePage.classList.remove('hidden');
    } else if (page === 'talent') {
        talentPage.classList.remove('hidden');
    } else if (page === 'rankings') {
        rankingsPage.classList.remove('hidden');
        loadRankings();
    } else if (page === 'auth') {
        authPage.classList.remove('hidden');
        initAuthPage();
    }
}

async function loadPlayers() {
    try {
        const response = await fetch('data/players.json');
        if (!response.ok) throw new Error('无法加载数据');
        players = await response.json();
        filteredPlayers = [...players];
        renderTeamTags();
        renderCards();
    } catch (error) {
        console.error('加载数据失败:', error);
        resultCount.textContent = '数据加载失败，请使用本地服务器运行';
    }
}

function renderTeamTags() {
    const teams = ['全部', ...new Set(players.map(p => p.teamAbbr))];
    
    teamTagsContainer.innerHTML = teams.map(team => `
        <button class="team-tag ${team === selectedTeam ? 'active' : ''}" data-team="${team}">
            ${team}
        </button>
    `).join('');
    
    teamTagsContainer.querySelectorAll('.team-tag').forEach(tag => {
        tag.addEventListener('click', () => {
            const team = tag.dataset.team;
            if (selectedTeam === team && team !== '全部') {
                selectedTeam = '全部';
            } else {
                selectedTeam = team;
            }
            updateTeamTagsUI();
            filterPlayers();
        });
    });
}

function updateTeamTagsUI() {
    teamTagsContainer.querySelectorAll('.team-tag').forEach(tag => {
        tag.classList.toggle('active', tag.dataset.team === selectedTeam);
    });
}

function filterPlayers() {
    filteredPlayers = players.filter(player => {
        const matchesSearch = searchQuery === '' || 
            player.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            (player.nickname && player.nickname.toLowerCase().includes(searchQuery.toLowerCase()));
        
        const matchesTeam = selectedTeam === '全部' || player.teamAbbr === selectedTeam;
        
        return matchesSearch && matchesTeam;
    });
    
    renderCards();
}

function debounce(func, delay) {
    return function(...args) {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => func.apply(this, args), delay);
    };
}

const debouncedFilter = debounce(() => {
    searchQuery = searchInput.value.trim();
    filterPlayers();
}, 300);

function renderCards() {
    resultCount.innerHTML = `找到 <strong>${filteredPlayers.length}</strong> 位球星`;
    
    if (filteredPlayers.length === 0) {
        cardsContainer.innerHTML = '';
        emptyState.classList.remove('hidden');
        return;
    }
    
    emptyState.classList.add('hidden');
    
    cardsContainer.innerHTML = filteredPlayers.map(player => `
        <article class="card" data-id="${player.id}">
            <div class="card-image-wrapper">
                <div class="card-loading" id="loading-${player.id}">加载中...</div>
                <img class="card-image" 
                     src="${player.profileImage}" 
                     alt="${player.name}"
                     onload="this.previousElementSibling.style.display='none'"
                     onerror="this.previousElementSibling.textContent='图片未找到'">
            </div>
            <div class="card-content">
                <h3 class="card-name">${player.name}</h3>
                ${player.nickname ? `<div class="card-nickname">"${player.nickname}"</div>` : ''}
                <div class="card-team">
                    <span class="team-abbr">${player.teamAbbr}</span>
                    ${player.team}
                </div>
            </div>
        </article>
    `).join('');
    
    cardsContainer.querySelectorAll('.card').forEach(card => {
        card.addEventListener('click', () => {
            const id = parseInt(card.dataset.id);
            const player = players.find(p => p.id === id);
            if (player) showDetail(player);
        });
    });
}

function showDetail(player) {
    homePage.classList.add('hidden');
    detailPage.classList.remove('hidden');
    window.scrollTo(0, 0);
    
    const detailImage = document.getElementById('detail-image');
    const detailImageLoading = document.getElementById('detail-image-loading');
    const detailGif = document.getElementById('detail-gif');
    const gifLoading = document.getElementById('gif-loading');
    
    detailImageLoading.style.display = 'flex';
    gifLoading.style.display = 'flex';
    
    detailImage.src = player.profileImage;
    detailImage.alt = player.name;
    detailImage.onload = () => detailImageLoading.style.display = 'none';
    detailImage.onerror = () => detailImageLoading.textContent = '图片未找到';
    
    detailGif.src = player.actionGif;
    detailGif.alt = player.actionDescription;
    detailGif.onload = () => gifLoading.style.display = 'none';
    detailGif.onerror = () => gifLoading.textContent = 'GIF未找到';
    
    document.getElementById('detail-name').textContent = player.name;
    document.getElementById('detail-nickname').textContent = player.nickname ? `"${player.nickname}"` : '';
    document.getElementById('detail-team').textContent = player.team;
    document.getElementById('detail-position').textContent = player.position;
    document.getElementById('detail-height').textContent = player.height;
    document.getElementById('detail-weight').textContent = player.weight;
    document.getElementById('detail-honors').textContent = player.honors;
    document.getElementById('detail-action-desc').textContent = player.actionDescription;
}

function showHome() {
    detailPage.classList.add('hidden');
    homePage.classList.remove('hidden');
    window.scrollTo(0, 0);
}

function clearFilters() {
    searchInput.value = '';
    searchQuery = '';
    selectedTeam = '全部';
    updateTeamTagsUI();
    filterPlayers();
}

talentForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const formData = new FormData(talentForm);
    const data = {
        nickname: formData.get('nickname'),
        height: parseFloat(formData.get('height')),
        weight: parseFloat(formData.get('weight')),
        armSpan: formData.get('armSpan') ? parseFloat(formData.get('armSpan')) : null,
        verticalJump: formData.get('verticalJump') ? parseFloat(formData.get('verticalJump')) : 65,
        runningJump: formData.get('runningJump') ? parseFloat(formData.get('runningJump')) : 80,
        position: formData.get('position') || null,
        playStyle: formData.getAll('playStyle')
    };

    try {
        const userId = DB.saveProfile(data);
        const result = analyzeTalent(data);
        DB.saveTalent(userId, result);
        showTalentResult(result);
    } catch (error) {
        console.error('分析失败:', error);
        alert('分析失败，请检查输入数据');
    }
});

function showTalentResult(result) {
    talentResult.classList.remove('hidden');
    
    const activeStar = result.matchedStarActive || {};
    const funStar = result.matchedStarFun || {};
    
    document.getElementById('result-star-active').textContent = 
        activeStar.nickname ? `${activeStar.name} "${activeStar.nickname}"` : activeStar.name || '未知';
    document.getElementById('result-star-desc').textContent = activeStar.description || '';
    
    document.getElementById('result-star-fun').textContent = 
        funStar.nickname ? `${funStar.nickname}` : funStar.name || '未知';
    document.getElementById('result-star-fun-desc').textContent = funStar.description || '';
    
    const scores = result.scores || {};
    const scoreNames = { shooting: '投射', speed: '速度', iq: '球商', handling: '运球', defense: '防守' };
    
    const scoreBars = document.getElementById('score-bars');
    scoreBars.innerHTML = Object.entries(scores).map(([key, value]) => `
        <div class="score-bar">
            <span class="score-label">${scoreNames[key] || key}</span>
            <div class="score-track">
                <div class="score-fill" style="width: ${value}%"></div>
            </div>
            <span class="score-value">${value}</span>
        </div>
    `).join('');
    
    const comments = result.comments || {};
    const commentsList = document.getElementById('comments-list');
    commentsList.innerHTML = Object.entries(comments).map(([key, text]) => `
        <div class="comment-item">${text}</div>
    `).join('');
    
    talentResult.scrollIntoView({ behavior: 'smooth' });
}

document.getElementById('retry-btn').addEventListener('click', () => {
    talentResult.classList.add('hidden');
    talentForm.reset();
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

function loadRankings() {
    try {
        const data = DB.getRankings(20);
        if (data.length > 0) {
            renderRankings(data);
        } else {
            rankingsList.innerHTML = '<div class="empty-state"><p class="empty-text">暂无数据，快去提交你的天赋分析吧！</p></div>';
        }
    } catch (error) {
        rankingsList.innerHTML = '<div class="empty-state"><p class="empty-text">数据加载失败</p></div>';
    }
}

function renderRankings(rankings) {
    rankingsList.innerHTML = rankings.map(item => `
        <div class="rank-item" data-user-id="${item.userId}">
            <div class="rank-number">${item.rank}</div>
            <div class="rank-info">
                <div class="rank-name">${item.nickname}</div>
                <div class="rank-meta">${item.height}cm | ${item.weight}kg | ${item.position || '未知位置'}</div>
            </div>
            <div class="rank-score">${item.totalScore}</div>
        </div>
    `).join('');
    
    rankingsList.querySelectorAll('.rank-item').forEach(item => {
        item.addEventListener('click', () => {
            const userId = item.dataset.userId;
            loadUserDetail(userId);
        });
    });
}

function loadUserDetail(userId) {
    try {
        const result = DB.getUserDetail(parseInt(userId));
        if (result) {
            showUserDetail(result);
        } else {
            alert('获取用户详情失败');
        }
    } catch (error) {
        console.error('加载失败:', error);
        alert('数据加载失败');
    }
}

function showUserDetail(data) {
    rankingsPage.classList.add('hidden');
    document.getElementById('user-detail-page').classList.remove('hidden');
    window.scrollTo(0, 0);
    
    const user = data.user;
    const talent = data.talent;
    
    document.getElementById('user-detail-name').textContent = user.nickname;
    document.getElementById('user-detail-height').textContent = `${user.height} cm`;
    document.getElementById('user-detail-weight').textContent = `${user.weight} kg`;
    document.getElementById('user-detail-armspan').textContent = user.armSpan ? `${user.armSpan} cm` : '未填写';
    document.getElementById('user-detail-position').textContent = user.position || '未填写';
    document.getElementById('user-detail-vertical').textContent = user.verticalJump ? `${user.verticalJump} cm` : '未填写';
    document.getElementById('user-detail-running').textContent = user.runningJump ? `${user.runningJump} cm` : '未填写';
    document.getElementById('user-detail-styles').textContent = user.playStyle && user.playStyle.length > 0 ? user.playStyle.join('、') : '未填写';
    
    if (talent) {
        const activeStar = talent.matchedStarActive || {};
        document.getElementById('matched-star-name').textContent = activeStar.name || '未知球星';
        document.getElementById('matched-star-nickname').textContent = activeStar.nickname ? `"${activeStar.nickname}"` : '';
        document.getElementById('matched-star-desc').textContent = activeStar.description || '';
        
        const scores = talent.scores || {};
        const scoreNames = { shooting: '投射', speed: '速度', iq: '球商', handling: '运球', defense: '防守' };
        
        const scoreBars = document.getElementById('user-score-bars');
        scoreBars.innerHTML = Object.entries(scores).map(([key, value]) => `
            <div class="score-bar">
                <span class="score-label">${scoreNames[key] || key}</span>
                <div class="score-track">
                    <div class="score-fill" style="width: ${value}%"></div>
                </div>
                <span class="score-value">${value}</span>
            </div>
        `).join('');
        
        const comments = talent.comments || {};
        const commentsEl = document.getElementById('user-comments');
        commentsEl.innerHTML = Object.entries(comments).map(([key, text]) => `
            <div class="comment-item">${text}</div>
        `).join('');
    }
}

document.getElementById('back-to-rankings').addEventListener('click', () => {
    document.getElementById('user-detail-page').classList.add('hidden');
    rankingsPage.classList.remove('hidden');
});

// ====== 认证页面逻辑 ======

let recoverState = { step: 1, nickname: '', resetToken: '' };

function initAuthPage() {
    loadSecurityQuestions();
    resetAuthForms();
    Auth.updateNavUI();
}

async function loadSecurityQuestions() {
    const select = document.getElementById('register-security-question');
    if (!select) return;
    try {
        const data = await Auth.getSecurityQuestions();
        if (data.success && data.data) {
            select.innerHTML = '<option value="">请选择密保问题</option>' +
                data.data.map(q => '<option value="' + q + '">' + q + '</option>').join('');
        }
    } catch {
        // 离线下使用默认列表
        const defaults = [
            "你最喜欢的篮球运动员是谁？",
            "你的小学校名是什么？",
            "你母亲的姓名是什么？",
            "你的出生城市是哪里？",
            "你最喜欢的运动是什么？",
            "你的第一个宠物的名字是什么？"
        ];
        select.innerHTML = '<option value="">请选择密保问题</option>' +
            defaults.map(q => '<option value="' + q + '">' + q + '</option>').join('');
    }
}

function resetAuthForms() {
    document.querySelectorAll('.auth-form').forEach(f => f.reset());
    document.querySelectorAll('.auth-message').forEach(el => { el.textContent = ''; el.className = 'auth-message'; });
    switchAuthTab('login');
    resetRecoverFlow();
}

function switchAuthTab(tab) {
    document.querySelectorAll('.auth-tab').forEach(t => t.classList.toggle('active', t.dataset.authTab === tab));
    document.querySelectorAll('.auth-panel').forEach(p => p.classList.toggle('active', p.id === 'auth-panel-' + tab));
    if (tab === 'recover') {
        resetRecoverFlow();
    }
}

function showMessage(containerId, text, type) {
    const el = document.getElementById(containerId);
    el.textContent = text;
    el.className = 'auth-message ' + (type === 'error' ? 'auth-error' : 'auth-success');
    if (type === 'success') {
        setTimeout(() => { el.textContent = ''; el.className = 'auth-message'; }, 3000);
    }
}

// 登录
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    const nickname = form.nickname.value.trim();
    const password = form.password.value;

    if (!nickname || !password) {
        showMessage('login-message', '请填写昵称和密码', 'error');
        return;
    }

    const submitBtn = form.querySelector('.auth-btn-submit');
    submitBtn.disabled = true;
    submitBtn.textContent = '登录中...';

    const data = await Auth.login(nickname, password);

    submitBtn.disabled = false;
    submitBtn.textContent = '登录';

    if (data.success) {
        Auth.updateNavUI();
        showMessage('login-message', '登录成功！', 'success');
        setTimeout(() => {
            switchPage('talent');
            navBtns.forEach(b => b.classList.remove('active'));
            document.querySelector('[data-page="talent"]').classList.add('active');
        }, 800);
    } else {
        showMessage('login-message', data.message || '登录失败', 'error');
    }
});

// 注册
document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    const nickname = form.nickname.value.trim();
    const password = form.password.value;
    const confirmPassword = form.confirmPassword.value;
    const securityQuestion = form.securityQuestion.value;
    const securityAnswer = form.securityAnswer.value.trim();

    if (!nickname || !password || !securityQuestion || !securityAnswer) {
        showMessage('register-message', '请填写所有必填项', 'error');
        return;
    }
    if (password !== confirmPassword) {
        showMessage('register-message', '两次密码输入不一致', 'error');
        return;
    }
    if (password.length < 4) {
        showMessage('register-message', '密码至少需要4个字符', 'error');
        return;
    }

    const submitBtn = form.querySelector('.auth-btn-submit');
    submitBtn.disabled = true;
    submitBtn.textContent = '注册中...';

    const data = await Auth.register(nickname, password, securityQuestion, securityAnswer);

    submitBtn.disabled = false;
    submitBtn.textContent = '注册';

    if (data.success) {
        Auth.updateNavUI();
        showMessage('register-message', '注册成功！', 'success');
        setTimeout(() => {
            switchPage('talent');
            navBtns.forEach(b => b.classList.remove('active'));
            document.querySelector('[data-page="talent"]').classList.add('active');
        }, 800);
    } else {
        showMessage('register-message', data.message || '注册失败', 'error');
    }
});

// Tab 切换
document.querySelectorAll('.auth-tab').forEach(tab => {
    tab.addEventListener('click', () => {
        switchAuthTab(tab.dataset.authTab);
    });
});

// 导航：登录/注册 ↔ 找回密码
document.getElementById('go-to-recover').addEventListener('click', () => {
    document.querySelectorAll('.auth-tab').forEach(t => t.classList.remove('active'));
    switchAuthTab('recover');
});
document.getElementById('go-to-register').addEventListener('click', () => switchAuthTab('register'));
document.getElementById('go-to-login').addEventListener('click', () => switchAuthTab('login'));
document.getElementById('go-back-to-login').addEventListener('click', () => {
    resetRecoverFlow();
    switchAuthTab('login');
});

// 找回密码流程
function resetRecoverFlow() {
    recoverState = { step: 1, nickname: '', resetToken: '' };
    document.getElementById('recover-step-1').classList.remove('hidden');
    document.getElementById('recover-step-2').classList.add('hidden');
    document.getElementById('recover-step-3').classList.add('hidden');
    document.getElementById('recover-submit-btn').textContent = '下一步';
    updateRecoverSteps(1);
    const msg = document.getElementById('recover-message');
    msg.textContent = '';
    msg.className = 'auth-message';
}

function updateRecoverSteps(activeStep) {
    document.querySelectorAll('.recover-step').forEach(el => {
        const step = parseInt(el.dataset.step);
        el.classList.remove('active', 'done');
        if (step < activeStep) el.classList.add('done');
        if (step === activeStep) el.classList.add('active');
    });
}

document.getElementById('recover-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const msgEl = document.getElementById('recover-message');
    const submitBtn = document.getElementById('recover-submit-btn');

    if (recoverState.step === 1) {
        const nickname = e.target.recoverNickname.value.trim();
        if (!nickname) {
            showMessage('recover-message', '请输入昵称', 'error');
            return;
        }
        submitBtn.disabled = true;
        submitBtn.textContent = '查询中...';
        const data = await Auth.forgotPassword(nickname);
        submitBtn.disabled = false;
        submitBtn.textContent = '下一步';

        if (data.success) {
            recoverState.nickname = nickname;
            recoverState.step = 2;
            document.getElementById('recover-step-1').classList.add('hidden');
            document.getElementById('recover-step-2').classList.remove('hidden');
            document.getElementById('recover-question-display').textContent = data.question;
            updateRecoverSteps(2);
            msgEl.textContent = '';
            msgEl.className = 'auth-message';
            e.target.securityAnswer.value = '';
        } else {
            showMessage('recover-message', data.message || '用户不存在', 'error');
        }
    } else if (recoverState.step === 2) {
        const answer = e.target.securityAnswer.value.trim();
        if (!answer) {
            showMessage('recover-message', '请输入密保答案', 'error');
            return;
        }
        submitBtn.disabled = true;
        submitBtn.textContent = '验证中...';
        const data = await Auth.verifyAnswer(recoverState.nickname, answer);
        submitBtn.disabled = false;
        submitBtn.textContent = '重置密码';

        if (data.success) {
            recoverState.resetToken = data.resetToken;
            recoverState.step = 3;
            document.getElementById('recover-step-2').classList.add('hidden');
            document.getElementById('recover-step-3').classList.remove('hidden');
            updateRecoverSteps(3);
            msgEl.textContent = '';
            msgEl.className = 'auth-message';
            e.target.newPassword.value = '';
        } else {
            showMessage('recover-message', data.message || '验证失败', 'error');
        }
    } else if (recoverState.step === 3) {
        const newPassword = e.target.newPassword.value;
        if (!newPassword || newPassword.length < 4) {
            showMessage('recover-message', '密码至少需要4个字符', 'error');
            return;
        }
        submitBtn.disabled = true;
        submitBtn.textContent = '重置中...';
        const data = await Auth.resetPassword(recoverState.nickname, recoverState.resetToken, newPassword);
        submitBtn.disabled = false;
        submitBtn.textContent = '完成';

        if (data.success) {
            showMessage('recover-message', '密码重置成功！请用新密码登录', 'success');
            setTimeout(() => {
                resetRecoverFlow();
                switchAuthTab('login');
            }, 1500);
        } else {
            showMessage('recover-message', data.message || '重置失败', 'error');
        }
    }
});

// 导航栏登录按钮
document.getElementById('nav-auth-btn').addEventListener('click', () => {
    if (Auth.isLoggedIn()) {
        if (confirm('确定要退出登录吗？')) {
            Auth.logout().then(() => {
                Auth.updateNavUI();
                switchPage('home');
                navBtns.forEach(b => b.classList.remove('active'));
                document.querySelector('[data-page="home"]').classList.add('active');
            });
        }
    } else {
        switchPage('auth');
        navBtns.forEach(b => b.classList.remove('active'));
    }
});

function init() {
    searchInput.addEventListener('input', debouncedFilter);
    clearFiltersBtn.addEventListener('click', clearFilters);
    backBtn.addEventListener('click', showHome);

    loadPlayers();
    Auth.updateNavUI();
}

document.addEventListener('DOMContentLoaded', init);
