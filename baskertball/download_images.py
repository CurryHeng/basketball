#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NBA 球星图片自动下载器
从多个公开源下载球员头像和动作图片
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
import os
import time
import requests
from pathlib import Path

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

PLAYERS = [
    {"id": 1, "name": "Stephen Curry", "search": "stephen curry", "wiki": "Stephen_Curry_(basketball)"},
    {"id": 2, "name": "LeBron James", "search": "lebron james", "wiki": "LeBron_James"},
    {"id": 3, "name": "Kevin Durant", "search": "kevin durant", "wiki": "Kevin_Durant"},
    {"id": 4, "name": "Giannis Antetokounmpo", "search": "giannis", "wiki": "Giannis_Antetokounmpo"},
    {"id": 5, "name": "Luka Doncic", "search": "luka doncic", "wiki": "Luka_Dončić"},
    {"id": 6, "name": "Joel Embiid", "search": "joel embiid", "wiki": "Joel_Embiid"},
    {"id": 7, "name": "Nikola Jokic", "search": "nikola jokic", "wiki": "Nikola_Jokić"},
    {"id": 8, "name": "Jayson Tatum", "search": "jayson tatum", "wiki": "Jayson_Tatum"},
    {"id": 9, "name": "Anthony Davis", "search": "anthony davis", "wiki": "Anthony_Davis_(basketball)"},
    {"id": 10, "name": "Kawhi Leonard", "search": "kawhi leonard", "wiki": "Kawhi_Leonard"},
    {"id": 11, "name": "Damian Lillard", "search": "damian lillard", "wiki": "Damian_Lillard"},
    {"id": 12, "name": "Shai Gilgeous-Alexander", "search": "shai gilgeous", "wiki": "Shai_Gilgeous-Alexander"},
    {"id": 13, "name": "Anthony Edwards", "search": "anthony edwards", "wiki": "Anthony_Edwards_(basketball)"},
    {"id": 14, "name": "Jalen Brunson", "search": "jalen brunson", "wiki": "Jalen_Brunson"},
    {"id": 15, "name": "Devin Booker", "search": "devin booker", "wiki": "Devin_Booker"},
    {"id": 16, "name": "Jimmy Butler", "search": "jimmy butler", "wiki": "Jimmy_Butler"},
    {"id": 17, "name": "Trae Young", "search": "trae young", "wiki": "Trae_Young"},
    {"id": 18, "name": "Kyrie Irving", "search": "kyrie irving", "wiki": "Kyrie_Irving"},
    {"id": 19, "name": "Bam Adebayo", "search": "bam adebayo", "wiki": "Bam_Adebayo"},
    {"id": 20, "name": "Klay Thompson", "search": "klay thompson", "wiki": "Klay_Thompson"},
    {"id": 21, "name": "Victor Wembanyama", "search": "victor wembanyama", "wiki": "Victor_Wembanyama"},
    {"id": 22, "name": "De'Aaron Fox", "search": "de'aaron fox", "wiki": "De'Aaron_Fox"},
    {"id": 23, "name": "Pascal Siakam", "search": "pascal siakam", "wiki": "Pascal_Siakam"},
    {"id": 24, "name": "Zion Williamson", "search": "zion williamson", "wiki": "Zion_Williamson"},
    {"id": 25, "name": "Jaren Jackson Jr.", "search": "jaren jackson", "wiki": "Jaren_Jackson_Jr."},
    {"id": 26, "name": "Ja Morant", "search": "ja morant", "wiki": "Ja_Morant"},
    {"id": 27, "name": "James Harden", "search": "james harden", "wiki": "James_Harden"},
    {"id": 28, "name": "Chris Paul", "search": "chris paul", "wiki": "Chris_Paul"},
    {"id": 29, "name": "Bradley Beal", "search": "bradley beal", "wiki": "Bradley_Beal"},
    {"id": 30, "name": "Jaylen Brown", "search": "jaylen brown", "wiki": "Jaylen_Brown_(basketball)"},
]

def create_directories():
    Path("images").mkdir(exist_ok=True)
    Path("gifs").mkdir(exist_ok=True)
    print("文件夹已创建: images/, gifs/")

def download_image(url, filepath, description="图片"):
    try:
        response = requests.get(url, headers=HEADERS, timeout=15, stream=True)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"  下载成功: {description}")
            return True
        else:
            print(f"  下载失败 ({response.status_code}): {description}")
            return False
    except Exception as e:
        print(f"  下载出错: {e}")
        return False

def get_wiki_image(wiki_name):
    sources = [
        f"https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/{wiki_name}.jpg/440px-{wiki_name}.jpg",
        f"https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/{wiki_name}.jpg/440px-{wiki_name}.jpg",
        f"https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/{wiki_name}.jpg/440px-{wiki_name}.jpg",
    ]
    for url in sources:
        try:
            resp = requests.head(url, headers=HEADERS, timeout=5, allow_redirects=True)
            if resp.status_code == 200 and 'image' in resp.headers.get('Content-Type', ''):
                return url
        except:
            continue
    return None

def search_google_image(query, search_type="face"):
    search_urls = [
        f"https://source.unsplash.com/400x400/?{query},basketball,portrait",
        f"https://ui-avatars.com/api/?name={query.replace(' ', '+')}&background=FF6B00&color=fff&size=400&bold=true",
    ]
    return search_urls[0]

def download_player_images(player):
    name = player['name']
    search = player['search']
    wiki = player['wiki']
    
    name_slug = name.lower().replace(' ', '_').replace("'", '').replace('.', '')
    profile_path = f"images/{name_slug}_profile.jpg"
    gif_path = f"gifs/{name_slug}_action.gif"
    
    print(f"\n[{player['id']}/{len(PLAYERS)}] {name}")
    
    profile_downloaded = False
    gif_downloaded = False
    
    wiki_url = get_wiki_image(wiki)
    if wiki_url:
        profile_downloaded = download_image(wiki_url, profile_path, "Wikipedia 头像")
    
    if not profile_downloaded:
        unsplash_url = f"https://source.unsplash.com/400x400/?{search},basketball,athlete"
        profile_downloaded = download_image(unsplash_url, profile_path, "Unsplash 头像")
    
    if not profile_downloaded:
        avatar_url = f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&background=FF6B00&color=fff&size=400&bold=true"
        profile_downloaded = download_image(avatar_url, profile_path, "头像占位图")
    
    gif_keywords = ["basketball", "dunk", "shoot", "slam"]
    for keyword in gif_keywords:
        gif_url = f"https://source.unsplash.com/600x400/?{search},{keyword},action"
        if download_image(gif_url, gif_path, f"动作图 ({keyword})"):
            gif_downloaded = True
            break
    
    if not gif_downloaded:
        placeholder_url = f"https://via.placeholder.com/600x400/1A1A1A/FF6B00?text={name.replace(' ', '+')}"
        download_image(placeholder_url, gif_path, "动作图占位符")
    
    return profile_path if profile_downloaded else None, gif_path if gif_downloaded else None

def main():
    print("=" * 60)
    print("NBA 球星图片自动下载器")
    print("=" * 60)
    
    create_directories()
    
    results = []
    
    for player in PLAYERS:
        profile, gif = download_player_images(player)
        results.append({
            'name': player['name'],
            'profile': profile,
            'gif': gif
        })
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print("下载完成!")
    print("=" * 60)
    
    success_count = sum(1 for r in results if r['profile'])
    print(f"\n成功下载: {success_count}/{len(PLAYERS)} 位球员头像")
    
    print("\n已下载文件:")
    print(f"  images/ 文件夹: {len(list(Path('images').glob('*')))} 个文件")
    print(f"  gifs/ 文件夹: {len(list(Path('gifs').glob('*')))} 个文件")

if __name__ == "__main__":
    main()
