# -*- coding: utf-8 -*-
"""
匹配规则配置 - 可自行修改调整
包含：球星模板库、评分权重、匹配逻辑
"""

# ==================== NBA球星模板库 ====================
# 现役版本模板
STAR_TEMPLATES_ACTIVE = [
    {
        "name": "Stephen Curry",
        "nickname": "萌神",
        "position": "PG",
        "height_range": (175, 195),
        "weight_range": (70, 95),
        "arm_span_ratio": (0.95, 1.05),
        "vertical_jump": (60, 80),
        "running_jump": (75, 95),
        "play_style": ["投射", "组织", "无球跑动"],
        "scores": {"shooting": 98, "speed": 88, "iq": 95, "handling": 90, "defense": 70},
        "description": "你拥有库里的灵魂！超远三分是你的武器，改变比赛的神射手！"
    },
    {
        "name": "LeBron James",
        "nickname": "小皇帝",
        "position": "SF",
        "height_range": (195, 215),
        "weight_range": (100, 130),
        "arm_span_ratio": (1.00, 1.15),
        "vertical_jump": (70, 90),
        "running_jump": (85, 110),
        "play_style": ["突破", "组织", "全能"],
        "scores": {"shooting": 85, "speed": 90, "iq": 98, "handling": 88, "defense": 88},
        "description": "天选之子！全能战士，坦克冲锋，球商拉满！"
    },
    {
        "name": "Kevin Durant",
        "nickname": "死神",
        "position": "SF",
        "height_range": (200, 215),
        "weight_range": (95, 115),
        "arm_span_ratio": (1.05, 1.20),
        "vertical_jump": (65, 85),
        "running_jump": (80, 100),
        "play_style": ["投射", "单打", "中距离"],
        "scores": {"shooting": 96, "speed": 82, "iq": 88, "handling": 92, "defense": 80},
        "description": "死神降临！无解中距离，镰刀挥舞，得分如探囊取物！"
    },
    {
        "name": "Giannis Antetokounmpo",
        "nickname": "字母哥",
        "position": "PF",
        "height_range": (200, 218),
        "weight_range": (100, 125),
        "arm_span_ratio": (1.08, 1.25),
        "vertical_jump": (75, 95),
        "running_jump": (90, 115),
        "play_style": ["突破", "防守", "快攻"],
        "scores": {"shooting": 70, "speed": 95, "iq": 80, "handling": 75, "defense": 95},
        "description": "希腊怪兽！禁区霸主，欧洲步暴扣震撼全场！"
    },
    {
        "name": "Nikola Jokic",
        "nickname": "小丑",
        "position": "C",
        "height_range": (205, 220),
        "weight_range": (115, 140),
        "arm_span_ratio": (1.00, 1.15),
        "vertical_jump": (50, 70),
        "running_jump": (60, 80),
        "play_style": ["组织", "低位", "策应"],
        "scores": {"shooting": 85, "speed": 60, "iq": 99, "handling": 80, "defense": 82},
        "description": "约基奇式中锋！鬼魅传球，塞尔维亚魔术师！"
    },
    {
        "name": "Joel Embiid",
        "nickname": "大帝",
        "position": "C",
        "height_range": (208, 220),
        "weight_range": (115, 140),
        "arm_span_ratio": (1.05, 1.18),
        "vertical_jump": (65, 85),
        "running_jump": (75, 95),
        "play_style": ["低位", "中距离", "防守"],
        "scores": {"shooting": 80, "speed": 65, "iq": 85, "handling": 70, "defense": 92},
        "description": "大帝降临！梦幻脚步，禁区统治力拉满！"
    },
    {
        "name": "Kyrie Irving",
        "nickname": "德鲁大叔",
        "position": "PG",
        "height_range": (180, 195),
        "weight_range": (75, 95),
        "arm_span_ratio": (0.95, 1.08),
        "vertical_jump": (70, 90),
        "running_jump": (85, 105),
        "play_style": ["单打", "运球", "终结"],
        "scores": {"shooting": 90, "speed": 92, "iq": 85, "handling": 98, "defense": 72},
        "description": "德鲁大叔！史诗级运球，街球艺术大师！"
    },
    {
        "name": "Anthony Edwards",
        "nickname": "蚁人",
        "position": "SG",
        "height_range": (188, 200),
        "weight_range": (90, 115),
        "arm_span_ratio": (1.00, 1.12),
        "vertical_jump": (85, 105),
        "running_jump": (100, 120),
        "play_style": ["突破", "暴扣", "投射"],
        "scores": {"shooting": 82, "speed": 94, "iq": 78, "handling": 85, "defense": 82},
        "description": "蚁人起飞！暴力美学扣将，新生代飞人！"
    },
]

# 养生娱乐版本模板
STAR_TEMPLATES_FUN = [
    {
        "name": "野球场霸主",
        "nickname": "老大爷",
        "description": "养生篮球创始人！靠智商吃饭，不跳也能赢！",
        "scores": {"shooting": 75, "speed": 40, "iq": 95, "handling": 70, "defense": 60}
    },
    {
        "name": "三分神射",
        "nickname": "炮台",
        "description": "站桩投手！全场跑动不超过10米，三分雨下个不停！",
        "scores": {"shooting": 95, "speed": 30, "iq": 70, "handling": 50, "defense": 40}
    },
    {
        "name": "内线巨兽",
        "nickname": "肉盾",
        "description": "吨位即正义！卡位大师，篮板收割机！",
        "scores": {"shooting": 40, "speed": 25, "iq": 70, "handling": 30, "defense": 90}
    },
    {
        "name": "花式运球王",
        "nickname": "街球手",
        "description": "动作花里胡哨，效果嘛...懂的都懂！",
        "scores": {"shooting": 60, "speed": 75, "iq": 55, "handling": 95, "defense": 35}
    },
    {
        "name": "快乐篮球人",
        "nickname": "气氛组",
        "description": "赢不赢不重要，姿势要帅，氛围要嗨！",
        "scores": {"shooting": 55, "speed": 55, "iq": 60, "handling": 55, "defense": 55}
    },
]

# ==================== 评分权重配置 ====================
SCORING_WEIGHTS = {
    "height": 0.15,
    "weight": 0.10,
    "arm_span": 0.15,
    "vertical_jump": 0.20,
    "running_jump": 0.20,
    "play_style_match": 0.20
}

# ==================== 天赋评分文案模板 ====================
# 可自行修改评价文案
TALENT_COMMENTS = {
    "shooting": {
        "high": "投篮姿势教科书级别，库里看了都想拜师！",
        "mid": "投射能力在线，继续磨练能成大器！",
        "low": "投还是传，这是个问题..."
    },
    "speed": {
        "high": "风一样的男子，快攻一打五不是梦！",
        "mid": "速度够用，追风少年在路上！",
        "low": "养生篮球爱好者，稳扎稳打也是一种战术！"
    },
    "iq": {
        "high": "球商爆表！隆多看了直呼内行！",
        "mid": "场上意识不错，继续积累经验！",
        "low": "多看比赛多思考，球商也是能练的！"
    },
    "handling": {
        "high": "运球如跳舞，欧文直呼内行！",
        "mid": "基本功扎实，继续磨练会更丝滑！",
        "low": "护球要紧，别轻易下球！"
    },
    "defense": {
        "high": "防守大闸！贝弗利附体，对手噩梦！",
        "mid": "防守态度积极，继续加油！",
        "low": "进攻是最好的防守？也许吧..."
    }
}

# ==================== 位置匹配规则 ====================
POSITION_MAP = {
    "控球后卫": "PG",
    "得分后卫": "SG",
    "小前锋": "SF",
    "大前锋": "PF",
    "中锋": "C",
    "PG": "PG",
    "SG": "SG",
    "SF": "SF",
    "PF": "PF",
    "C": "C"
}

# ==================== 打法风格映射 ====================
PLAY_STYLE_KEYWORDS = {
    "投射": ["投篮", "三分", "投射", "远投", "中投"],
    "突破": ["突破", "过人", "冲框", "上篮", "抛投"],
    "组织": ["传球", "组织", "策应", "助攻", "控场"],
    "防守": ["防守", "盖帽", "抢断", "篮板", "护框"],
    "单打": ["单打", "1v1", "iso", "背打", "干拔"],
    "低位": ["低位", "背打", "勾手", "内线"],
    "暴扣": ["扣篮", "暴扣", "空接"],
    "运球": ["运球", "花式", "变向"],
    "无球跑动": ["跑位", "无球", "空切"],
    "快攻": ["快攻", "反击", "转换"],
    "中距离": ["中投", "中距离", "干拔"],
    "终结": ["终结", "上篮", "抛投"],
    "全能": ["全能", "什么都会", "六边形"]
}
