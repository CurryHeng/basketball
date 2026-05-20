#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新 players.json 使用下载好的本地图片
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
from pathlib import Path

PLAYER_DATABASE = [
    {"id": 1, "name": "Stephen Curry", "nickname": "萌神", "team": "Golden State Warriors", "teamAbbr": "GSW", "position": "Point Guard", "height": "6'2\"", "weight": "185 lbs", "honors": "2x MVP, 4x NBA Champion, 1x Finals MVP, 10x All-Star", "action": "招牌超远距离三分投篮，改变篮球时代的神射手", "image_slug": "curry", "gif_slug": "curry_shoot"},
    {"id": 2, "name": "LeBron James", "nickname": "小皇帝", "team": "Los Angeles Lakers", "teamAbbr": "LAL", "position": "Small Forward", "height": "6'9\"", "weight": "250 lbs", "honors": "4x MVP, 4x NBA Champion, 4x Finals MVP, 20x All-Star", "action": "霸道坦克式突破暴扣，全能战士的终极武器", "image_slug": "lebron", "gif_slug": "lebron_dunk"},
    {"id": 3, "name": "Kevin Durant", "nickname": "死神", "team": "Phoenix Suns", "teamAbbr": "PHX", "position": "Small Forward", "height": "6'11\"", "weight": "240 lbs", "honors": "1x MVP, 2x NBA Champion, 2x Finals MVP, 14x All-Star", "action": "无解中距离干拔跳投，死神镰刀挥舞瞬间", "image_slug": "durant", "gif_slug": "durant_shoot"},
    {"id": 4, "name": "Giannis Antetokounmpo", "nickname": "字母哥", "team": "Milwaukee Bucks", "teamAbbr": "MIL", "position": "Power Forward", "height": "6'11\"", "weight": "242 lbs", "honors": "2x MVP, 1x NBA Champion, 1x Finals MVP, 8x All-Star", "action": "希腊怪兽欧洲步暴扣，禁区霸主的毁灭冲击", "image_slug": "giannis", "gif_slug": "giannis_dunk"},
    {"id": 5, "name": "Luka Doncic", "nickname": "魔术师", "team": "Dallas Mavericks", "teamAbbr": "DAL", "position": "Point Guard", "height": "6'7\"", "weight": "230 lbs", "honors": "5x All-Star, 4x All-NBA First Team, Rookie of the Year", "action": "神奇后撤步三分，斯洛文尼亚天才的魔法时刻", "image_slug": "luka", "gif_slug": "luka_stepback"},
    {"id": 6, "name": "Joel Embiid", "nickname": "大帝", "team": "Philadelphia 76ers", "teamAbbr": "PHI", "position": "Center", "height": "7'0\"", "weight": "280 lbs", "honors": "1x MVP, 7x All-Star, 3x All-Defensive First Team", "action": "梦幻脚步内线进攻，喀麦隆大帝的禁区统治", "image_slug": "joel_embiid"},
    {"id": 7, "name": "Nikola Jokic", "nickname": "小丑", "team": "Denver Nuggets", "teamAbbr": "DEN", "position": "Center", "height": "7'0\"", "weight": "284 lbs", "honors": "3x MVP, 1x NBA Champion, 1x Finals MVP, 6x All-Star", "action": "鬼魅不看人传球，塞尔维亚天才的中锋魔术", "image_slug": "nikola_jokic"},
    {"id": 8, "name": "Jayson Tatum", "nickname": "獭兔", "team": "Boston Celtics", "teamAbbr": "BOS", "position": "Small Forward", "height": "6'8\"", "weight": "210 lbs", "honors": "1x NBA Champion, 5x All-Star, 4x All-NBA", "action": "丝滑后撤步中投，绿军新王的得分盛宴", "image_slug": "jayson_tatum"},
    {"id": 9, "name": "Anthony Davis", "nickname": "浓眉", "team": "Los Angeles Lakers", "teamAbbr": "LAL", "position": "Power Forward", "height": "6'10\"", "weight": "253 lbs", "honors": "1x NBA Champion, 10x All-Star, 4x All-Defensive First Team", "action": "遮天蔽日大火锅，浓眉哥的防守禁区", "image_slug": "anthony_davis"},
    {"id": 10, "name": "Kawhi Leonard", "nickname": "卡哇伊", "team": "Los Angeles Clippers", "teamAbbr": "LAC", "position": "Small Forward", "height": "6'7\"", "weight": "225 lbs", "honors": "2x NBA Champion, 2x Finals MVP, 6x All-Star, 2x DPOY", "action": "机器人般精准中投，沉默杀手的致命一击", "image_slug": "kawhi_leonard"},
    {"id": 11, "name": "Damian Lillard", "nickname": "利指导", "team": "Milwaukee Bucks", "teamAbbr": "MIL", "position": "Point Guard", "height": "6'2\"", "weight": "195 lbs", "honors": "8x All-Star, NBA 75th Anniversary Team", "action": "Logo超远三分绝杀，利拉德时间的致命时刻", "image_slug": "damian_lillard"},
    {"id": 12, "name": "Shai Gilgeous-Alexander", "nickname": "SGA", "team": "Oklahoma City Thunder", "teamAbbr": "OKC", "position": "Point Guard", "height": "6'6\"", "weight": "195 lbs", "honors": "2x All-Star, 2x All-NBA First Team", "action": "蛇形突破撕裂防线，加拿大新星崛起之路", "image_slug": "shai_gilgeous-alexander"},
    {"id": 13, "name": "Anthony Edwards", "nickname": "蚁人", "team": "Minnesota Timberwolves", "teamAbbr": "MIN", "position": "Shooting Guard", "height": "6'4\"", "weight": "225 lbs", "honors": "2x All-Star, Most Improved Player Candidate", "action": "暴力美学扣篮，新生代飞人的震撼表演", "image_slug": "anthony_edwards"},
    {"id": 14, "name": "Jalen Brunson", "nickname": "布伦森", "team": "New York Knicks", "teamAbbr": "NYK", "position": "Point Guard", "height": "6'1\"", "weight": "190 lbs", "honors": "1x All-Star, 1x All-NBA Second Team", "action": "关键时刻大心脏，纽约新王的领袖气质", "image_slug": "jalen_brunson"},
    {"id": 15, "name": "Devin Booker", "nickname": "布克", "team": "Phoenix Suns", "teamAbbr": "PHX", "position": "Shooting Guard", "height": "6'6\"", "weight": "206 lbs", "honors": "4x All-Star, 70-Point Game Record", "action": "丝滑中距离投篮，太阳神射手的得分盛宴", "image_slug": "devin_booker"},
    {"id": 16, "name": "Jimmy Butler", "nickname": "吉米巴", "team": "Miami Heat", "teamAbbr": "MIA", "position": "Small Forward", "height": "6'7\"", "weight": "230 lbs", "honors": "6x All-Star, 5x All-Defensive, 2x Finals Appearance", "action": "季后赛模式觉醒，硬汉 Butler 的关键时刻", "image_slug": "jimmy_butler"},
    {"id": 17, "name": "Trae Young", "nickname": "吹羊", "team": "Atlanta Hawks", "teamAbbr": "ATL", "position": "Point Guard", "height": "6'1\"", "weight": "164 lbs", "honors": "3x All-Star, 1x All-NBA, Finals Appearance", "action": "超远三分加抛投，冰吹羊的得分武器库", "image_slug": "trae_young"},
    {"id": 18, "name": "Kyrie Irving", "nickname": "德鲁大叔", "team": "Dallas Mavericks", "teamAbbr": "DAL", "position": "Point Guard", "height": "6'2\"", "weight": "195 lbs", "honors": "1x NBA Champion, 8x All-Star, 50-40-90 Club", "action": "史诗级运球过人，德鲁大叔的街球艺术", "image_slug": "kyrie_irving"},
    {"id": 19, "name": "Bam Adebayo", "nickname": "阿德巴约", "team": "Miami Heat", "teamAbbr": "MIA", "position": "Center", "height": "6'9\"", "weight": "255 lbs", "honors": "3x All-Star, 5x All-Defensive, 2x Finals Appearance", "action": "全能防守大闸，热火铁壁的禁区守护", "image_slug": "bam_adebayo"},
    {"id": 20, "name": "Klay Thompson", "nickname": "汤神", "team": "Dallas Mavericks", "teamAbbr": "DAL", "position": "Shooting Guard", "height": "6'6\"", "weight": "215 lbs", "honors": "4x NBA Champion, 5x All-Star, Single-Game 14 Threes Record", "action": "接球就投三分雨，水花兄弟的经典时刻", "image_slug": "klay_thompson"},
    {"id": 21, "name": "Victor Wembanyama", "nickname": "文班亚马", "team": "San Antonio Spurs", "teamAbbr": "SAS", "position": "Center", "height": "7'4\"", "weight": "210 lbs", "honors": "Rookie of the Year, Blocks Leader, All-Rookie First Team", "action": "外星人般的全能身手，法国独角兽的惊艳首秀", "image_slug": "victor_wembanyama"},
    {"id": 22, "name": "De'Aaron Fox", "nickname": "福克斯", "team": "Sacramento Kings", "teamAbbr": "SAC", "position": "Point Guard", "height": "6'3\"", "weight": "185 lbs", "honors": "1x All-Star, 1x All-NBA Third Team, Clutch Player of the Year", "action": "闪电突破撕裂防线，联盟最快的后卫冲刺", "image_slug": "deaaron_fox"},
    {"id": 23, "name": "Pascal Siakam", "nickname": "西亚卡姆", "team": "Indiana Pacers", "teamAbbr": "IND", "position": "Power Forward", "height": "6'9\"", "weight": "230 lbs", "honors": "1x NBA Champion, 2x All-Star, Most Improved Player", "action": "丝滑转身突破，喀麦隆前锋的全面进化", "image_slug": "pascal_siakam"},
    {"id": 24, "name": "Zion Williamson", "nickname": "胖虎", "team": "New Orleans Pelicans", "teamAbbr": "NOP", "position": "Power Forward", "height": "6'6\"", "weight": "284 lbs", "honors": "1x All-Star, All-Rookie First Team", "action": "暴力美学隔人暴扣，胖虎的重型坦克冲击", "image_slug": "zion_williamson"},
    {"id": 25, "name": "Ja Morant", "nickname": "贾莫兰特", "team": "Memphis Grizzlies", "teamAbbr": "MEM", "position": "Point Guard", "height": "6'3\"", "weight": "174 lbs", "honors": "2x All-Star, Rookie of the Year, Most Improved Player", "action": "炸裂弹跳暴扣，灰熊少主的空中漫步", "image_slug": "ja_morant"},
    {"id": 26, "name": "James Harden", "nickname": "大胡子", "team": "LA Clippers", "teamAbbr": "LAC", "position": "Shooting Guard", "height": "6'5\"", "weight": "220 lbs", "honors": "1x MVP, 10x All-Star, 3x Scoring Champion, 2x Assist Leader", "action": "后撤步三分大师，大胡子的得分艺术", "image_slug": "james_harden"},
    {"id": 27, "name": "Chris Paul", "nickname": "CP3", "team": "San Antonio Spurs", "teamAbbr": "SAS", "position": "Point Guard", "height": "6'0\"", "weight": "175 lbs", "honors": "12x All-Star, 11x All-NBA, 9x All-Defensive, 5x Assist Leader", "action": "控场大师传球艺术，CP3的球队大脑", "image_slug": "chris_paul"},
    {"id": 28, "name": "Bradley Beal", "nickname": "比尔", "team": "Phoenix Suns", "teamAbbr": "PHX", "position": "Shooting Guard", "height": "6'4\"", "weight": "207 lbs", "honors": "3x All-Star, 2x All-NBA Third Team", "action": "丝滑得分机器，比尔的全面进攻武器", "image_slug": "bradley_beal"},
    {"id": 29, "name": "Jaylen Brown", "nickname": "杰伦布朗", "team": "Boston Celtics", "teamAbbr": "BOS", "position": "Shooting Guard", "height": "6'6\"", "weight": "223 lbs", "honors": "3x All-Star, 1x NBA Champion, 1x All-NBA", "action": "暴力扣加强硬防守，绿军双探花之二", "image_slug": "jaylen_brown"},
    {"id": 30, "name": "Jaren Jackson Jr.", "nickname": "三勾", "team": "Memphis Grizzlies", "teamAbbr": "MEM", "position": "Power Forward", "height": "6'11\"", "weight": "242 lbs", "honors": "1x DPOY, 1x All-Star, 2x Blocks Leader", "action": "护框加三分的空间内线，灰熊防守核心", "image_slug": "jaren_jackson"},
]

TEAM_COLORS = {
    "GSW": ("FF6B00", "FFFFFF"), "LAL": ("552583", "FDB927"), "PHX": ("E56020", "FFFFFF"),
    "MIL": ("00471B", "EEE1C6"), "DAL": ("00538C", "FFFFFF"), "PHI": ("006BB6", "F58D26"),
    "DEN": ("0E2240", "FEC524"), "BOS": ("007A33", "FFFFFF"), "LAC": ("C8102E", "FFFFFF"),
    "OKC": ("007AC1", "FFFFFF"), "MIN": ("0E2340", "78BE20"), "NYK": ("F58426", "003DA5"),
    "MIA": ("98002E", "FFA938"), "ATL": ("E03A3E", "C1D32F"), "SAS": ("C4CED4", "000000"),
    "SAC": ("5A2D81", "637271"), "IND": ("002D62", "FDBB30"), "NOP": ("0C2340", "E31837"),
    "MEM": ("5D76A9", "12173D"),
}

def find_image(slug):
    patterns = [
        f"images/{slug}_profile.jpg",
        f"images/{slug}.jpg",
        f"images/{slug}_profile.png",
        f"images/{slug}.png",
    ]
    for p in patterns:
        if Path(p).exists():
            return p
    return None

def find_gif(slug):
    patterns = [
        f"gifs/{slug}.gif",
        f"gifs/{slug}_action.gif",
    ]
    for p in patterns:
        if Path(p).exists():
            return p
    return None

def main():
    print("=" * 60)
    print("更新球员数据（使用本地图片）")
    print("=" * 60)
    
    players = []
    
    for p in PLAYER_DATABASE:
        team_color = TEAM_COLORS.get(p['teamAbbr'], ("FF6B00", "FFFFFF"))
        image_slug = p.get('image_slug', p['name'].lower().replace(' ', '_').replace("'", '').replace('.', ''))
        gif_slug = p.get('gif_slug', image_slug)
        
        local_image = find_image(image_slug)
        local_gif = find_gif(gif_slug)
        
        if local_image:
            profile_img = local_image
            status = "本地图片"
        else:
            profile_img = f"https://ui-avatars.com/api/?name={p['name'].replace(' ', '+')}&background={team_color[0]}&color={team_color[1]}&size=400&bold=true"
            status = "在线头像"
        
        if local_gif:
            action_gif = local_gif
        else:
            action_gif = f"https://via.placeholder.com/600x400/{team_color[0]}/{team_color[1]}?text=Action"
        
        player = {
            "id": p['id'],
            "name": p['name'],
            "nickname": p['nickname'],
            "team": p['team'],
            "teamAbbr": p['teamAbbr'],
            "position": p['position'],
            "height": p['height'],
            "weight": p['weight'],
            "honors": p['honors'],
            "profileImage": profile_img,
            "actionGif": action_gif,
            "actionDescription": p['action']
        }
        players.append(player)
        
        img_status = "本地" if local_image else "在线"
        gif_status = "本地" if local_gif else "在线"
        print(f"  [{p['id']:2d}] {p['name']:25s} | 头像:{img_status} | 动作:{gif_status}")
    
    with open('data/players.json', 'w', encoding='utf-8') as f:
        json.dump(players, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print(f"已保存 {len(players)} 位球员数据")
    
    local_images = sum(1 for p in players if p['profileImage'].startswith('images/'))
    local_gifs = sum(1 for p in players if p['actionGif'].startswith('gifs/'))
    print(f"本地图片: {local_images} | 本地动作: {local_gifs}")

if __name__ == "__main__":
    main()
