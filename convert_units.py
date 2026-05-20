#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
转换身高体重为双单位制（英制 + 公制）
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json

def feet_inches_to_cm(height_str):
    """将英尺英寸转换为厘米，如 6'2" -> 188"""
    try:
        parts = height_str.replace('"', '').split("'")
        feet = int(parts[0])
        inches = int(parts[1]) if len(parts) > 1 else 0
        cm = feet * 30.48 + inches * 2.54
        return round(cm)
    except:
        return None

def lbs_to_kg(weight_str):
    """将磅转换为公斤，如 185 lbs -> 84"""
    try:
        lbs = int(weight_str.replace(' lbs', ''))
        kg = lbs * 0.4536
        return round(kg)
    except:
        return None

def convert_height(height_str):
    """转换身高为双单位制"""
    cm = feet_inches_to_cm(height_str)
    if cm:
        return f'{height_str} ({cm} cm)'
    return height_str

def convert_weight(weight_str):
    """转换体重为双单位制"""
    kg = lbs_to_kg(weight_str)
    if kg:
        return f'{weight_str} ({kg} kg)'
    return weight_str

def main():
    print("=" * 60)
    print("转换身高体重为双单位制")
    print("=" * 60)
    
    with open('data/players.json', 'r', encoding='utf-8') as f:
        players = json.load(f)
    
    for p in players:
        old_height = p['height']
        old_weight = p['weight']
        
        p['height'] = convert_height(old_height)
        p['weight'] = convert_weight(old_weight)
        
        print(f"  {p['name']:25s} | {old_height} -> {p['height']:20s} | {old_weight} -> {p['weight']}")
    
    with open('data/players.json', 'w', encoding='utf-8') as f:
        json.dump(players, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print(f"已更新 {len(players)} 位球员数据")

if __name__ == "__main__":
    main()
