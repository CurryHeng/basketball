# -*- coding: utf-8 -*-
"""
球星图片搜索下载器
支持多个免费图片API：Unsplash、Pexels、Pixabay

API Key 配置方式（优先级从高到低）：
1. 环境变量: UNSPLASH_KEY, PEXELS_KEY, PIXABAY_KEY
2. .env 文件: 项目根目录下的 .env 文件
3. config.ini 文件: 项目根目录下的 config.ini 文件
"""

import os
import sys
import time
import requests
from pathlib import Path

# ==================== API Key 配置 ====================

def load_api_keys():
    """
    加载 API Key，按优先级尝试多种方式
    返回: dict
    """
    keys = {
        'unsplash': None,
        'pexels': None,
        'pixabay': None
    }
    
    # 方式1: 环境变量
    keys['unsplash'] = os.environ.get('UNSPLASH_KEY')
    keys['pexels'] = os.environ.get('PEXELS_KEY')
    keys['pixabay'] = os.environ.get('PIXABAY_KEY')
    
    # 方式2: .env 文件
    env_file = Path(__file__).parent / '.env'
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip().upper()
                    value = value.strip()
                    if key == 'UNSPLASH_ACCESS_KEY' and not keys['unsplash']:
                        keys['unsplash'] = value
                    elif key == 'PEXELS_API_KEY' and not keys['pexels']:
                        keys['pexels'] = value
                    elif key == 'PIXABAY_API_KEY' and not keys['pixabay']:
                        keys['pixabay'] = value
    
    # 方式3: config.ini 文件
    config_file = Path(__file__).parent / 'config.ini'
    if config_file.exists():
        try:
            import configparser
            config = configparser.ConfigParser()
            config.read(config_file, encoding='utf-8')
            if 'API' in config:
                if not keys['unsplash'] and config['API'].get('unsplash'):
                    keys['unsplash'] = config['API']['unsplash']
                if not keys['pexels'] and config['API'].get('pexels'):
                    keys['pexels'] = config['API']['pexels']
                if not keys['pixabay'] and config['API'].get('pixabay'):
                    keys['pixabay'] = config['API']['pixabay']
        except:
            pass
    
    return keys

# 加载 API Keys
API_KEYS = load_api_keys()
UNSPLASH_ACCESS_KEY = API_KEYS['unsplash']

# 图片保存目录
IMAGES_DIR = Path(__file__).parent.parent / 'images'

# 请求超时时间
TIMEOUT = 10

# 请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}


def ensure_dir():
    """确保图片目录存在"""
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✅ 图片保存目录: {IMAGES_DIR}")


def search_unsplash(query, count=10):
    """
    从Unsplash搜索图片
    API文档: https://unsplash.com/documentation
    """
    print(f"\n🔍 Unsplash搜索: {query}")
    
    # 使用Unsplash的source API（无需API Key的免费接口）
    # 或者使用官方API（需要API Key）
    
    if UNSPLASH_ACCESS_KEY and UNSPLASH_ACCESS_KEY != 'YOUR_UNSPLASH_ACCESS_KEY':
        # 官方API方式
        url = 'https://api.unsplash.com/search/photos'
        params = {
            'query': query,
            'per_page': count,
            'client_id': UNSPLASH_ACCESS_KEY
        }
        
        try:
            response = requests.get(url, params=params, timeout=TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get('results', []):
                results.append({
                    'id': item['id'],
                    'url': item['urls']['regular'],
                    'thumbnail': item['urls']['thumb'],
                    'description': item.get('description') or item.get('alt_description', ''),
                    'source': 'unsplash',
                    'author': item['user']['name'],
                    'download_url': item['urls']['full']
                })
            
            print(f"  找到 {len(results)} 张图片")
            return results
            
        except requests.exceptions.Timeout:
            print("  ❌ 请求超时")
            return []
        except requests.exceptions.RequestException as e:
            print(f"  ❌ 请求失败: {e}")
            return []
    else:
        # 无API Key时使用随机图片接口
        print("  ⚠️ 未配置Unsplash API Key，使用随机图片模式")
        return get_unsplash_random(query, count)


def get_unsplash_random(query, count=10):
    """Unsplash随机图片接口（无需API Key）"""
    results = []
    
    for i in range(count):
        # Unsplash Source API: https://source.unsplash.com/
        # 格式: https://source.unsplash.com/400x400/?basketball,player
        width, height = 400, 400
        url = f"https://source.unsplash.com/{width}x{height}/?{query},basketball,sports"
        
        results.append({
            'id': f'unsplash_random_{i}_{int(time.time())}',
            'url': url,
            'thumbnail': f"https://source.unsplash.com/100x100/?{query},basketball",
            'description': f'{query} 篮球图片 {i+1}',
            'source': 'unsplash_random',
            'author': 'Unsplash',
            'download_url': f"https://source.unsplash.com/600x600/?{query},basketball,sports"
        })
    
    print(f"  生成 {len(results)} 个随机图片链接")
    return results


def search_pexels(query, count=10):
    """
    从Pexels搜索图片
    API文档: https://www.pexels.com/api/documentation/
    """
    api_key = API_KEYS['pexels']
    
    if not api_key or api_key == 'YOUR_PEXELS_API_KEY':
        print(f"\n⚠️ Pexels: 未配置API Key，跳过")
        return []
    
    print(f"\n🔍 Pexels搜索: {query}")
    
    url = 'https://api.pexels.com/v1/search'
    headers = {'Authorization': api_key}
    params = {
        'query': f'{query} basketball',
        'per_page': count,
        'page': 1
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get('photos', []):
            results.append({
                'id': str(item['id']),
                'url': item['src']['large'],
                'thumbnail': item['src']['tiny'],
                'description': item.get('alt', '') or item.get('photographer', ''),
                'source': 'pexels',
                'author': item['photographer'],
                'download_url': item['src']['original']
            })
        
        print(f"  找到 {len(results)} 张图片")
        return results
        
    except requests.exceptions.Timeout:
        print("  ❌ 请求超时")
        return []
    except requests.exceptions.RequestException as e:
        print(f"  ❌ 请求失败: {e}")
        return []


def search_pixabay(query, count=10):
    """
    从Pixabay搜索图片
    API文档: https://pixabay.com/api/docs/
    """
    api_key = API_KEYS['pixabay']
    
    if not api_key or api_key == 'YOUR_PIXABAY_API_KEY':
        print(f"\n⚠️ Pixabay: 未配置API Key，跳过")
        return []
    
    print(f"\n🔍 Pixabay搜索: {query}")
    
    url = 'https://pixabay.com/api/'
    params = {
        'key': api_key,
        'q': f'{query} basketball',
        'image_type': 'photo',
        'per_page': count,
        'safesearch': 'true'
    }
    
    try:
        response = requests.get(url, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get('hits', []):
            results.append({
                'id': str(item['id']),
                'url': item['webformatURL'],
                'thumbnail': item['previewURL'],
                'description': item.get('tags', ''),
                'source': 'pixabay',
                'author': item.get('user', ''),
                'download_url': item['largeImageURL']
            })
        
        print(f"  找到 {len(results)} 张图片")
        return results
        
    except requests.exceptions.Timeout:
        print("  ❌ 请求超时")
        return []
    except requests.exceptions.RequestException as e:
        print(f"  ❌ 请求失败: {e}")
        return []


def download_image(url, filename, show_progress=True):
    """
    下载单张图片
    参数:
        url: 图片URL
        filename: 保存文件名
        show_progress: 是否显示进度
    返回:
        成功返回文件路径，失败返回None
    """
    filepath = IMAGES_DIR / filename
    
    try:
        if show_progress:
            print(f"  📥 下载中: {filename}")
        
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT, stream=True)
        response.raise_for_status()
        
        # 检查是否是图片
        content_type = response.headers.get('Content-Type', '')
        if 'image' not in content_type and not url.startswith('https://source.unsplash.com'):
            print(f"  ❌ 不是图片文件: {content_type}")
            return None
        
        # 写入文件
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        file_size = filepath.stat().st_size
        print(f"  ✅ 下载成功: {filename} ({file_size/1024:.1f} KB)")
        print(f"     保存路径: {filepath}")
        
        return str(filepath)
        
    except requests.exceptions.Timeout:
        print(f"  ❌ 下载超时: {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"  ❌ 下载失败: {e}")
        return None
    except IOError as e:
        print(f"  ❌ 文件写入失败: {e}")
        return None


def search_all(query, count=5):
    """从所有API搜索图片"""
    all_results = []
    
    # Unsplash
    all_results.extend(search_unsplash(query, count))
    
    # Pexels（需API Key）
    all_results.extend(search_pexels(query, count))
    
    # Pixabay（需API Key）
    all_results.extend(search_pixabay(query, count))
    
    return all_results


def download_batch(results, prefix='player'):
    """批量下载图片"""
    print(f"\n📥 开始批量下载 {len(results)} 张图片...")
    
    downloaded = []
    
    for i, item in enumerate(results, 1):
        filename = f"{prefix}_{item['source']}_{item['id']}.jpg"
        
        # 尝试下载大图，失败则尝试普通尺寸
        url = item.get('download_url') or item.get('url')
        result = download_image(url, filename)
        
        if result:
            downloaded.append({
                'filename': filename,
                'path': result,
                'info': item
            })
        else:
            # 重试普通URL
            result = download_image(item['url'], filename)
            if result:
                downloaded.append({
                    'filename': filename,
                    'path': result,
                    'info': item
                })
        
        # 避免请求过快
        time.sleep(0.5)
    
    print(f"\n✅ 成功下载: {len(downloaded)}/{len(results)} 张")
    return downloaded


def main():
    """主函数"""
    print("=" * 60)
    print("🏀 球星图片搜索下载器")
    print("=" * 60)
    
    ensure_dir()
    
    # 预设的球星搜索关键词
    star_players = [
        'stephen curry',
        'lebron james', 
        'kevin durant',
        'giannis antetokounmpo',
        'luka doncic',
        'michael jordan',
        'kobe bryant',
    ]
    
    print("\n📋 预设球星列表:")
    for i, name in enumerate(star_players, 1):
        print(f"  {i}. {name}")
    
    # 选择模式
    print("\n请选择模式:")
    print("  1. 搜索单个球星")
    print("  2. 批量下载所有预设球星")
    print("  3. 自定义搜索")
    
    choice = input("\n请输入选项 (1/2/3): ").strip()
    
    if choice == '1':
        # 搜索单个
        idx = int(input("请输入球星序号 (1-7): ")) - 1
        if 0 <= idx < len(star_players):
            query = star_players[idx]
            results = search_all(query, count=5)
            
            if results:
                download = input("\n是否下载这些图片? (y/n): ").lower()
                if download == 'y':
                    prefix = query.replace(' ', '_')
                    download_batch(results, prefix)
    
    elif choice == '2':
        # 批量下载
        for name in star_players:
            print(f"\n{'='*40}")
            results = search_all(name, count=3)
            if results:
                prefix = name.replace(' ', '_')
                download_batch(results, prefix)
            time.sleep(1)
    
    elif choice == '3':
        # 自定义搜索
        query = input("请输入搜索关键词: ").strip()
        if query:
            count = int(input("下载数量 (默认5): ") or 5)
            results = search_all(query, count=count)
            
            if results:
                download = input("\n是否下载这些图片? (y/n): ").lower()
                if download == 'y':
                    prefix = query.replace(' ', '_')
                    download_batch(results, prefix)
    
    print("\n" + "=" * 60)
    print("🎉 完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
