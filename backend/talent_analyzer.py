# -*- coding: utf-8 -*-
"""
天赋匹配核心逻辑
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config.matching_rules import (
    STAR_TEMPLATES_ACTIVE,
    STAR_TEMPLATES_FUN,
    SCORING_WEIGHTS,
    TALENT_COMMENTS,
    POSITION_MAP,
    PLAY_STYLE_KEYWORDS
)

def parse_play_style(style_input):
    """解析打法风格输入"""
    if isinstance(style_input, list):
        styles = style_input
    elif isinstance(style_input, str):
        styles = [s.strip() for s in style_input.replace('，', ',').split(',')]
    else:
        styles = []
    
    matched_styles = []
    for style in styles:
        for key, keywords in PLAY_STYLE_KEYWORDS.items():
            if any(kw in style.lower() for kw in keywords):
                matched_styles.append(key)
    
    return list(set(matched_styles)) if matched_styles else ["全能"]

def calculate_height_score(height_cm, template):
    """计算身高匹配分数"""
    min_h, max_h = template['height_range']
    if min_h <= height_cm <= max_h:
        return 100
    elif height_cm < min_h:
        return max(0, 100 - (min_h - height_cm) * 2)
    else:
        return max(0, 100 - (height_cm - max_h) * 2)

def calculate_weight_score(weight_kg, template):
    """计算体重匹配分数"""
    min_w, max_w = template['weight_range']
    if min_w <= weight_kg <= max_w:
        return 100
    elif weight_kg < min_w:
        return max(0, 100 - (min_w - weight_kg) * 3)
    else:
        return max(0, 100 - (weight_kg - max_w) * 3)

def calculate_jump_score(vertical, running, template):
    """计算弹跳匹配分数"""
    v_min, v_max = template['vertical_jump']
    r_min, r_max = template['running_jump']
    
    v_score = 100 if v_min <= vertical <= v_max else max(0, 100 - abs(vertical - (v_min + v_max) / 2) * 2)
    r_score = 100 if r_min <= running <= r_max else max(0, 100 - abs(running - (r_min + r_max) / 2) * 2)
    
    return (v_score + r_score) / 2

def calculate_style_match(user_styles, template_styles):
    """计算打法风格匹配分数"""
    if not user_styles or not template_styles:
        return 50
    
    matches = len(set(user_styles) & set(template_styles))
    total = len(set(user_styles) | set(template_styles))
    
    return (matches / total) * 100 if total > 0 else 50

def match_star_active(user_data):
    """匹配现役NBA球星模板"""
    height_cm = user_data.get('height', 180)
    weight_kg = user_data.get('weight', 75)
    arm_span = user_data.get('armSpan', height_cm * 1.02)
    vertical_jump = user_data.get('verticalJump', 65)
    running_jump = user_data.get('runningJump', 80)
    play_styles = parse_play_style(user_data.get('playStyle', []))
    
    best_match = None
    best_score = 0
    
    for template in STAR_TEMPLATES_ACTIVE:
        h_score = calculate_height_score(height_cm, template)
        w_score = calculate_weight_score(weight_kg, template)
        j_score = calculate_jump_score(vertical_jump, running_jump, template)
        s_score = calculate_style_match(play_styles, template.get('play_style', []))
        
        total = (
            h_score * SCORING_WEIGHTS['height'] +
            w_score * SCORING_WEIGHTS['weight'] +
            j_score * (SCORING_WEIGHTS['vertical_jump'] + SCORING_WEIGHTS['running_jump']) +
            s_score * SCORING_WEIGHTS['play_style_match']
        )
        
        if total > best_score:
            best_score = total
            best_match = template.copy()
            best_match['match_score'] = round(total, 1)
    
    return best_match

def match_star_fun(user_data):
    """匹配养生娱乐版本模板"""
    import random
    
    play_styles = parse_play_style(user_data.get('playStyle', []))
    
    if '投射' in play_styles or '投篮' in str(play_styles):
        return STAR_TEMPLATES_FUN[1]
    elif '防守' in play_styles:
        return STAR_TEMPLATES_FUN[0]
    elif '运球' in play_styles:
        return STAR_TEMPLATES_FUN[3]
    else:
        return random.choice(STAR_TEMPLATES_FUN)

def calculate_talent_scores(user_data, matched_template):
    """计算各项天赋分数"""
    base_scores = matched_template.get('scores', {
        "shooting": 70, "speed": 70, "iq": 70, "handling": 70, "defense": 70
    })
    
    height = user_data.get('height', 180)
    weight = user_data.get('weight', 75)
    vertical = user_data.get('verticalJump', 65)
    running = user_data.get('runningJump', 80)
    
    modifier = (vertical / 80 + running / 100) / 2
    
    scores = {}
    for key, base in base_scores.items():
        adjusted = base * (0.8 + modifier * 0.4)
        scores[key] = min(99, max(1, int(adjusted)))
    
    return scores

def generate_comments(scores):
    """生成趣味评价文案"""
    comments = {}
    
    for key, score in scores.items():
        if key in TALENT_COMMENTS:
            if score >= 85:
                level = 'high'
            elif score >= 60:
                level = 'mid'
            else:
                level = 'low'
            comments[key] = TALENT_COMMENTS[key][level]
    
    total = sum(scores.values()) / len(scores)
    if total >= 85:
        comments['overall'] = f"天赋异禀！综合评分 {total:.1f}，NBA球探已关注！"
    elif total >= 70:
        comments['overall'] = f"潜力股！综合评分 {total:.1f}，野球场称霸指日可待！"
    elif total >= 55:
        comments['overall'] = f"基本功扎实！综合评分 {total:.1f}，继续努力！"
    else:
        comments['overall'] = f"快乐篮球！综合评分 {total:.1f}，重在参与嘛！"
    
    return comments

def analyze_talent(user_data):
    """主分析函数：完整天赋分析"""
    matched_active = match_star_active(user_data)
    matched_fun = match_star_fun(user_data)
    
    scores = calculate_talent_scores(user_data, matched_active)
    comments = generate_comments(scores)
    
    result = {
        'matchedStar': matched_active['name'] if matched_active else '未知球星',
        'matchedStarActive': {
            'name': matched_active['name'],
            'nickname': matched_active['nickname'],
            'description': matched_active['description'],
            'matchScore': matched_active.get('match_score', 0)
        } if matched_active else {},
        'matchedStarFun': {
            'name': matched_fun['name'],
            'nickname': matched_fun['nickname'],
            'description': matched_fun['description']
        },
        'scores': scores,
        'comments': comments,
        'totalScore': round(sum(scores.values()) / len(scores), 1)
    }
    
    return result
