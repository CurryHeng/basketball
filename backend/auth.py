# -*- coding: utf-8 -*-
"""
用户认证模块 - 注册、登录、密码找回、昵称修改
"""

import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from backend.database import (
    create_user,
    get_user_by_nickname,
    get_user_by_id,
    create_session,
    get_session_by_token,
    delete_session,
    update_user_nickname,
    update_user_password
)

SECURITY_QUESTIONS = [
    "你最喜欢的篮球运动员是谁？",
    "你的小学校名是什么？",
    "你母亲的姓名是什么？",
    "你的出生城市是哪里？",
    "你最喜欢的运动是什么？",
    "你的第一个宠物的名字是什么？"
]

RESET_TOKENS = {}


def _generate_token():
    return secrets.token_hex(32)


def register(nickname, password, security_question, security_answer):
    """注册新用户，返回 (success, message, user_id)"""
    nickname = nickname.strip()
    if not nickname or len(nickname) < 1:
        return False, "昵称不能为空", None
    if len(nickname) > 20:
        return False, "昵称不能超过20个字符", None
    if not password or len(password) < 4:
        return False, "密码至少需要4个字符", None
    if not security_answer or len(security_answer.strip()) < 1:
        return False, "密保答案不能为空", None

    password_hash = generate_password_hash(password)
    answer_hash = generate_password_hash(security_answer.strip())

    user_id = create_user(nickname, password_hash, security_question, answer_hash)
    if user_id is None:
        return False, "该昵称已被注册，请换一个", None

    return True, "注册成功", user_id


def login(nickname, password):
    """登录，返回 (success, message, token, user)"""
    user = get_user_by_nickname(nickname.strip())
    if not user:
        return False, "用户不存在", None, None
    if not check_password_hash(user['password_hash'], password):
        return False, "密码错误", None, None

    token = _generate_token()
    create_session(user['id'], token)

    return True, "登录成功", token, {
        'id': user['id'],
        'nickname': user['nickname'],
        'createdAt': user['created_at']
    }


def logout(token):
    """登出"""
    delete_session(token)
    return True, "已退出登录"


def get_security_question(nickname):
    """获取用户的密保问题，不返回答案"""
    user = get_user_by_nickname(nickname.strip())
    if not user:
        return False, "用户不存在", None
    return True, user['security_question'], None


def verify_security_answer(nickname, security_answer):
    """验证密保答案，返回一次性重置 token"""
    user = get_user_by_nickname(nickname.strip())
    if not user:
        return False, "用户不存在", None
    if not check_password_hash(user['security_answer_hash'], security_answer.strip()):
        return False, "密保答案错误", None

    reset_token = _generate_token()
    RESET_TOKENS[reset_token] = user['id']
    return True, "验证成功", reset_token


def reset_password(nickname, reset_token, new_password):
    """使用重置 token 修改密码"""
    user_id = RESET_TOKENS.pop(reset_token, None)
    if user_id is None:
        return False, "重置令牌无效或已过期", None

    user = get_user_by_id(user_id)
    if not user or user['nickname'] != nickname.strip():
        return False, "用户信息不匹配", None
    if not new_password or len(new_password) < 4:
        return False, "密码至少需要4个字符", None

    password_hash = generate_password_hash(new_password)
    update_user_password(user_id, password_hash)
    return True, "密码重置成功", None


def change_nickname(user_id, new_nickname):
    """修改昵称"""
    new_nickname = new_nickname.strip()
    if not new_nickname or len(new_nickname) < 1:
        return False, "昵称不能为空"
    if len(new_nickname) > 20:
        return False, "昵称不能超过20个字符"

    ok = update_user_nickname(user_id, new_nickname)
    if not ok:
        return False, "该昵称已被使用"
    return True, "昵称修改成功"


def get_user_by_token(token):
    """通过 token 获取用户信息，用于鉴权"""
    session = get_session_by_token(token)
    if not session:
        return None
    return {
        'id': session['user_id'],
        'nickname': session['nickname']
    }
