// 本地存储数据库（替代 SQLite + Flask 后端）

const DB = {
    _read(key) {
        try { return JSON.parse(localStorage.getItem(key)) || []; }
        catch { return []; }
    },
    _write(key, data) {
        localStorage.setItem(key, JSON.stringify(data));
    },

    // 保存用户档案，返回用户ID
    saveProfile(data) {
        const users = this._read('bb_users');
        const id = users.length > 0 ? Math.max(...users.map(u => u.id)) + 1 : 1;
        const record = {
            id,
            nickname: data.nickname || '匿名球手',
            height: data.height,
            weight: data.weight,
            armSpan: data.armSpan || null,
            verticalJump: data.verticalJump || null,
            runningJump: data.runningJump || null,
            position: data.position || null,
            playStyle: data.playStyle || [],
            createdAt: new Date().toISOString()
        };
        users.push(record);
        this._write('bb_users', users);
        return id;
    },

    // 保存天赋分析结果
    saveTalent(userId, result) {
        const talents = this._read('bb_talents');
        talents.push({
            id: talents.length + 1,
            userId,
            matchedStar: result.matchedStar,
            matchedStarActive: result.matchedStarActive,
            matchedStarFun: result.matchedStarFun,
            scores: result.scores,
            comments: result.comments,
            totalScore: result.totalScore,
            createdAt: new Date().toISOString()
        });
        this._write('bb_talents', talents);
    },

    // 获取排行榜
    getRankings(limit = 20) {
        const users = this._read('bb_users');
        const talents = this._read('bb_talents');
        const latestTalents = {};
        for (const t of talents) {
            if (!latestTalents[t.userId] || new Date(t.createdAt) > new Date(latestTalents[t.userId].createdAt)) {
                latestTalents[t.userId] = t;
            }
        }
        const rankings = Object.values(latestTalents)
            .sort((a, b) => b.totalScore - a.totalScore)
            .slice(0, limit);
        return rankings.map((t, i) => {
            const user = users.find(u => u.id === t.userId) || {};
            return {
                rank: i + 1,
                userId: t.userId,
                nickname: user.nickname || '未知',
                height: user.height,
                weight: user.weight,
                position: user.position,
                totalScore: t.totalScore
            };
        });
    },

    // 获取用户详情
    getUserDetail(userId) {
        const users = this._read('bb_users');
        const talents = this._read('bb_talents');
        const user = users.find(u => u.id === userId);
        if (!user) return null;
        const userTalents = talents.filter(t => t.userId === userId)
            .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
        return {
            user,
            talent: userTalents.length > 0 ? userTalents[0] : null,
            history: userTalents
        };
    },

    // 获取所有用户
    getAllUsers() {
        return this._read('bb_users').sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
    }
};