// 天赋分析引擎（纯前端版）

function parsePlayStyle(styleInput) {
    if (!styleInput || (Array.isArray(styleInput) && styleInput.length === 0)) {
        return ["全能"];
    }
    const styles = Array.isArray(styleInput) ? styleInput
        : styleInput.replace(/，/g, ',').split(',').map(s => s.trim());

    const matched = [];
    for (const style of styles) {
        for (const [key, keywords] of Object.entries(PLAY_STYLE_KEYWORDS)) {
            if (keywords.some(kw => style.toLowerCase().includes(kw))) {
                matched.push(key);
            }
        }
    }
    return [...new Set(matched)].length > 0 ? [...new Set(matched)] : ["全能"];
}

function calcHeightScore(heightCm, template) {
    const [minH, maxH] = template.height_range;
    if (heightCm >= minH && heightCm <= maxH) return 100;
    if (heightCm < minH) return Math.max(0, 100 - (minH - heightCm) * 2);
    return Math.max(0, 100 - (heightCm - maxH) * 2);
}

function calcWeightScore(weightKg, template) {
    const [minW, maxW] = template.weight_range;
    if (weightKg >= minW && weightKg <= maxW) return 100;
    if (weightKg < minW) return Math.max(0, 100 - (minW - weightKg) * 3);
    return Math.max(0, 100 - (weightKg - maxW) * 3);
}

function calcJumpScore(vertical, running, template) {
    const [vMin, vMax] = template.vertical_jump;
    const [rMin, rMax] = template.running_jump;
    const vScore = (vertical >= vMin && vertical <= vMax) ? 100
        : Math.max(0, 100 - Math.abs(vertical - (vMin + vMax) / 2) * 2);
    const rScore = (running >= rMin && running <= rMax) ? 100
        : Math.max(0, 100 - Math.abs(running - (rMin + rMax) / 2) * 2);
    return (vScore + rScore) / 2;
}

function calcStyleMatch(userStyles, templateStyles) {
    if (!userStyles.length || !templateStyles.length) return 50;
    const intersection = userStyles.filter(s => templateStyles.includes(s));
    const union = [...new Set([...userStyles, ...templateStyles])];
    return (intersection.length / union.length) * 100;
}

function matchStarActive(userData) {
    const heightCm = userData.height || 180;
    const weightKg = userData.weight || 75;
    const verticalJump = userData.verticalJump || 65;
    const runningJump = userData.runningJump || 80;
    const playStyles = parsePlayStyle(userData.playStyle);

    let bestMatch = null;
    let bestScore = 0;

    for (const template of STAR_TEMPLATES_ACTIVE) {
        const hScore = calcHeightScore(heightCm, template);
        const wScore = calcWeightScore(weightKg, template);
        const jScore = calcJumpScore(verticalJump, runningJump, template);
        const sScore = calcStyleMatch(playStyles, template.play_style || []);

        const total = hScore * SCORING_WEIGHTS.height +
            wScore * SCORING_WEIGHTS.weight +
            jScore * (SCORING_WEIGHTS.vertical_jump + SCORING_WEIGHTS.running_jump) +
            sScore * SCORING_WEIGHTS.play_style_match;

        if (total > bestScore) {
            bestScore = total;
            bestMatch = { ...template, match_score: Math.round(total * 10) / 10 };
        }
    }
    return bestMatch;
}

function matchStarFun(userData) {
    const playStyles = parsePlayStyle(userData.playStyle);
    if (playStyles.includes("投射")) return STAR_TEMPLATES_FUN[1];
    if (playStyles.includes("防守")) return STAR_TEMPLATES_FUN[0];
    if (playStyles.includes("运球")) return STAR_TEMPLATES_FUN[3];
    return STAR_TEMPLATES_FUN[Math.floor(Math.random() * STAR_TEMPLATES_FUN.length)];
}

function calcTalentScores(userData, template) {
    const baseScores = template.scores || { shooting: 70, speed: 70, iq: 70, handling: 70, defense: 70 };
    const vertical = userData.verticalJump || 65;
    const running = userData.runningJump || 80;
    const modifier = (vertical / 80 + running / 100) / 2;

    const scores = {};
    for (const [key, base] of Object.entries(baseScores)) {
        scores[key] = Math.min(99, Math.max(1, Math.round(base * (0.8 + modifier * 0.4))));
    }
    return scores;
}

function generateComments(scores) {
    const comments = {};
    for (const [key, score] of Object.entries(scores)) {
        if (!TALENT_COMMENTS[key]) continue;
        const level = score >= 85 ? 'high' : score >= 60 ? 'mid' : 'low';
        comments[key] = TALENT_COMMENTS[key][level];
    }
    const avg = Object.values(scores).reduce((a, b) => a + b, 0) / Object.values(scores).length;
    if (avg >= 85) comments.overall = `天赋异禀！综合评分 ${avg.toFixed(1)}，NBA球探已关注！`;
    else if (avg >= 70) comments.overall = `潜力股！综合评分 ${avg.toFixed(1)}，野球场称霸指日可待！`;
    else if (avg >= 55) comments.overall = `基本功扎实！综合评分 ${avg.toFixed(1)}，继续努力！`;
    else comments.overall = `快乐篮球！综合评分 ${avg.toFixed(1)}，重在参与嘛！`;
    return comments;
}

function analyzeTalent(userData) {
    const matchedActive = matchStarActive(userData);
    const matchedFun = matchStarFun(userData);
    const scores = calcTalentScores(userData, matchedActive);
    const comments = generateComments(scores);

    return {
        matchedStar: matchedActive ? matchedActive.name : '未知球星',
        matchedStarActive: matchedActive ? {
            name: matchedActive.name,
            nickname: matchedActive.nickname,
            description: matchedActive.description,
            matchScore: matchedActive.match_score
        } : {},
        matchedStarFun: {
            name: matchedFun.name,
            nickname: matchedFun.nickname,
            description: matchedFun.description
        },
        scores: scores,
        comments: comments,
        totalScore: Math.round(Object.values(scores).reduce((a, b) => a + b, 0) / Object.values(scores).length * 10) / 10
    };
}