# -*- coding: utf-8 -*-
"""
Flask主应用 - 篮球天赋分析后端
极简轻量化设计，方便二次开发
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.database import (
    init_db,
    save_user_profile,
    save_talent_score,
    get_rankings,
    get_user_history,
    get_all_users,
    get_user_detail
)
from backend.talent_analyzer import analyze_talent
from backend.auth import (
    register,
    login,
    logout,
    get_security_question,
    verify_security_answer,
    reset_password,
    change_nickname,
    get_user_by_token,
    SECURITY_QUESTIONS
)

app = Flask(__name__)

CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route('/')
def index():
    """首页"""
    return jsonify({
        'message': '篮球天赋分析API',
        'version': '1.0.0',
        'endpoints': [
            'POST /api/analyze - 提交数据并分析天赋',
            'GET /api/rankings - 获取排行榜',
            'GET /api/users - 获取所有用户',
            'GET /api/user/<user_id> - 获取用户详情',
            'GET /api/history/<user_id> - 获取用户历史',
            'POST /api/video/upload - 预留视频上传接口',
            'POST /api/duel/compare - 预留双人对比接口'
        ]
    })

@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    """
    核心接口：接收用户数据，分析天赋
    请求数据格式：
    {
        "nickname": "用户昵称",
        "height": 185,          // 身高cm
        "weight": 75,           // 体重kg
        "armSpan": 190,         // 臂展cm（可选）
        "verticalJump": 65,     // 原地弹跳cm（可选）
        "runningJump": 80,      // 助跑弹跳cm（可选）
        "position": "PG",       // 位置（可选）
        "playStyle": ["投射", "突破"]  // 打法风格（可选）
    }
    """
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'})
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': '请求数据为空'}), 400
        
        required_fields = ['height', 'weight']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'缺少必填字段: {field}'}), 400
        
        user_id = save_user_profile(data)
        
        result = analyze_talent(data)
        
        save_talent_score(user_id, result)
        
        return jsonify({
            'success': True,
            'userId': user_id,
            'result': result
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rankings', methods=['GET'])
def rankings():
    """
    获取天赋排行榜
    参数: limit - 返回条数，默认10
    """
    try:
        limit = request.args.get('limit', 10, type=int)
        data = get_rankings(limit)
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users', methods=['GET'])
def users():
    """获取所有用户列表（用于双人对比选择）"""
    try:
        data = get_all_users()
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history/<int:user_id>', methods=['GET'])
def history(user_id):
    """获取用户历史记录"""
    try:
        data = get_user_history(user_id)
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/<int:user_id>', methods=['GET'])
def user_detail(user_id):
    """获取用户完整详情（用于排行榜点击查看）"""
    try:
        data = get_user_detail(user_id)
        if data:
            return jsonify({
                'success': True,
                'data': data
            })
        else:
            return jsonify({'error': '用户不存在'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/video/upload', methods=['POST', 'OPTIONS'])
def video_upload():
    """
    预留接口：视频上传
    TODO: 后续可接入AI视觉识别
    """
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'})
    
    return jsonify({
        'success': False,
        'message': '视频上传功能开发中，敬请期待！',
        'hint': '此接口预留用于AI动作识别'
    })

@app.route('/api/duel/compare', methods=['POST', 'OPTIONS'])
def duel_compare():
    """
    预留接口：双人动作对比
    请求数据格式:
    {
        "user1Id": 1,
        "user2Id": 2
    }
    TODO: 后续可开发对比分析功能
    """
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'})
    
    try:
        data = request.get_json()
        
        return jsonify({
            'success': False,
            'message': '双人对比功能开发中，敬请期待！',
            'hint': '此接口预留用于双人天赋对比',
            'receivedData': data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/config/templates', methods=['GET'])
def get_templates():
    """获取球星模板列表（方便前端展示）"""
    from backend.config.matching_rules import STAR_TEMPLATES_ACTIVE, STAR_TEMPLATES_FUN

    active = [{'name': t['name'], 'nickname': t['nickname'], 'position': t['position']}
              for t in STAR_TEMPLATES_ACTIVE]
    fun = [{'name': t['name'], 'nickname': t['nickname']}
           for t in STAR_TEMPLATES_FUN]

    return jsonify({
        'success': True,
        'active': active,
        'fun': fun
    })


# ========== 认证接口 ==========

def _get_user_from_header():
    """从 Authorization header 中解析用户"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None
    token = auth_header[7:]
    return get_user_by_token(token)


@app.route('/api/auth/security-questions', methods=['GET'])
def get_security_questions():
    """获取预设密保问题列表"""
    return jsonify({
        'success': True,
        'data': SECURITY_QUESTIONS
    })


@app.route('/api/auth/register', methods=['POST', 'OPTIONS'])
def auth_register():
    """注册"""
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'})

    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': '请求数据为空'}), 400

        ok, msg, user_id = register(
            data.get('nickname', ''),
            data.get('password', ''),
            data.get('securityQuestion', ''),
            data.get('securityAnswer', '')
        )

        status_code = 200 if ok else 400
        result = {'success': ok, 'message': msg}
        if user_id:
            result['userId'] = user_id
        return jsonify(result), status_code

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def auth_login():
    """登录"""
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'})

    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': '请求数据为空'}), 400

        ok, msg, token, user = login(
            data.get('nickname', ''),
            data.get('password', '')
        )

        status_code = 200 if ok else 400
        result = {'success': ok, 'message': msg}
        if token:
            result['token'] = token
            result['user'] = user
        return jsonify(result), status_code

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/auth/logout', methods=['POST', 'OPTIONS'])
def auth_logout():
    """登出"""
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'})

    try:
        token = request.headers.get('Authorization', '')
        if token.startswith('Bearer '):
            token = token[7:]
            ok, msg = logout(token)
        else:
            ok, msg = False, "未提供有效令牌"

        status_code = 200 if ok else 400
        return jsonify({'success': ok, 'message': msg}), status_code

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/auth/forgot-password', methods=['POST', 'OPTIONS'])
def auth_forgot_password():
    """找回密码 - 获取密保问题"""
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'})

    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': '请求数据为空'}), 400

        ok, msg, _ = get_security_question(data.get('nickname', ''))

        status_code = 200 if ok else 400
        result = {'success': ok}
        if ok:
            result['question'] = msg
        else:
            result['message'] = msg
        return jsonify(result), status_code

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/auth/verify-answer', methods=['POST', 'OPTIONS'])
def auth_verify_answer():
    """验证密保答案"""
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'})

    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': '请求数据为空'}), 400

        ok, msg, reset_token = verify_security_answer(
            data.get('nickname', ''),
            data.get('securityAnswer', '')
        )

        status_code = 200 if ok else 400
        result = {'success': ok, 'message': msg}
        if reset_token:
            result['resetToken'] = reset_token
        return jsonify(result), status_code

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/auth/reset-password', methods=['POST', 'OPTIONS'])
def auth_reset_password():
    """重置密码"""
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'})

    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': '请求数据为空'}), 400

        ok, msg, _ = reset_password(
            data.get('nickname', ''),
            data.get('resetToken', ''),
            data.get('newPassword', '')
        )

        status_code = 200 if ok else 400
        return jsonify({'success': ok, 'message': msg}), status_code

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/auth/change-nickname', methods=['POST', 'OPTIONS'])
def auth_change_nickname():
    """修改昵称"""
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'})

    try:
        user = _get_user_from_header()
        if not user:
            return jsonify({'success': False, 'message': '请先登录'}), 401

        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': '请求数据为空'}), 400

        ok, msg = change_nickname(user['id'], data.get('newNickname', ''))

        status_code = 200 if ok else 400
        return jsonify({'success': ok, 'message': msg}), status_code

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/auth/me', methods=['GET'])
def auth_me():
    """获取当前用户信息"""
    try:
        user = _get_user_from_header()
        if not user:
            return jsonify({'success': False, 'message': '未登录'}), 401

        return jsonify({'success': True, 'user': user})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


if __name__ == '__main__':
    init_db()

    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'

    print("=" * 50)
    print("篮球天赋分析后端启动")
    print(f"端口: {port}")
    print("=" * 50)

    app.run(host='0.0.0.0', port=port, debug=debug)
