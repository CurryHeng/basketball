import { getStore } from "@netlify/blobs";
import crypto from "crypto";

const SECURITY_QUESTIONS = [
  "你最喜欢的篮球运动员是谁？",
  "你的小学校名是什么？",
  "你母亲的姓名是什么？",
  "你的出生城市是哪里？",
  "你最喜欢的运动是什么？",
  "你的第一个宠物的名字是什么？",
];

function hashPassword(password) {
  const salt = crypto.randomBytes(16).toString("hex");
  const hash = crypto
    .pbkdf2Sync(password, salt, 100000, 64, "sha512")
    .toString("hex");
  return `${salt}:${hash}`;
}

function verifyPassword(password, stored) {
  const [salt, hash] = stored.split(":");
  const verify = crypto
    .pbkdf2Sync(password, salt, 100000, 64, "sha512")
    .toString("hex");
  return hash === verify;
}

function generateToken() {
  return crypto.randomBytes(32).toString("hex");
}

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "Content-Type, Authorization",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    },
  });
}

async function getUsers() {
  const store = getStore("basketball-auth");
  const raw = await store.get("users");
  return raw ? JSON.parse(raw) : [];
}

async function saveUsers(users) {
  const store = getStore("basketball-auth");
  await store.set("users", JSON.stringify(users));
}

async function getSessions() {
  const store = getStore("basketball-auth");
  const raw = await store.get("sessions");
  return raw ? JSON.parse(raw) : {};
}

async function saveSessions(sessions) {
  const store = getStore("basketball-auth");
  await store.set("sessions", JSON.stringify(sessions));
}

function getUserByToken(sessions, token) {
  return sessions[token] || null;
}

function parseAction(rawUrl) {
  const path = new URL(rawUrl).pathname;
  // path: /.netlify/functions/auth/login → action: login
  const parts = path.replace(/\/$/, "").split("/");
  return parts[parts.length - 1];
}

// ====== Route Handlers ======

async function handleGetSecurityQuestions() {
  return json({ success: true, data: SECURITY_QUESTIONS });
}

async function handleRegister(body) {
  const { nickname, password, securityQuestion, securityAnswer } = body;
  const name = (nickname || "").trim();

  if (!name || name.length > 20) {
    return json({ success: false, message: "昵称不能为空且不超过20个字符" }, 400);
  }
  if (!password || password.length < 4) {
    return json({ success: false, message: "密码至少需要4个字符" }, 400);
  }
  if (!securityAnswer || !securityAnswer.trim()) {
    return json({ success: false, message: "密保答案不能为空" }, 400);
  }

  const users = await getUsers();
  if (users.find((u) => u.nickname === name)) {
    return json({ success: false, message: "该昵称已被注册，请换一个" }, 400);
  }

  const user = {
    id: users.length > 0 ? Math.max(...users.map((u) => u.id)) + 1 : 1,
    nickname: name,
    passwordHash: hashPassword(password),
    securityQuestion,
    securityAnswerHash: hashPassword(securityAnswer.trim()),
    createdAt: new Date().toISOString(),
  };

  users.push(user);
  await saveUsers(users);

  // 注册后自动登录
  const token = generateToken();
  const sessions = await getSessions();
  sessions[token] = { userId: user.id, nickname: user.nickname };
  await saveSessions(sessions);

  return json({
    success: true,
    message: "注册成功",
    token,
    user: { id: user.id, nickname: user.nickname, createdAt: user.createdAt },
  });
}

async function handleLogin(body) {
  const { nickname, password } = body;
  const name = (nickname || "").trim();

  const users = await getUsers();
  const user = users.find((u) => u.nickname === name);

  if (!user) {
    return json({ success: false, message: "用户不存在" }, 400);
  }
  if (!verifyPassword(password, user.passwordHash)) {
    return json({ success: false, message: "密码错误" }, 400);
  }

  const token = generateToken();
  const sessions = await getSessions();
  sessions[token] = { userId: user.id, nickname: user.nickname };
  await saveSessions(sessions);

  return json({
    success: true,
    message: "登录成功",
    token,
    user: { id: user.id, nickname: user.nickname, createdAt: user.createdAt },
  });
}

async function handleLogout(request) {
  const auth = request.headers.get("authorization") || "";
  const token = auth.startsWith("Bearer ") ? auth.slice(7) : "";
  if (token) {
    const sessions = await getSessions();
    delete sessions[token];
    await saveSessions(sessions);
  }
  return json({ success: true, message: "已退出登录" });
}

async function handleForgotPassword(body) {
  const { nickname } = body;
  const name = (nickname || "").trim();
  const users = await getUsers();
  const user = users.find((u) => u.nickname === name);
  if (!user) {
    return json({ success: false, message: "用户不存在" }, 400);
  }
  return json({ success: true, question: user.securityQuestion });
}

async function handleVerifyAnswer(body) {
  const { nickname, securityAnswer } = body;
  const name = (nickname || "").trim();
  const users = await getUsers();
  const user = users.find((u) => u.nickname === name);

  if (!user) {
    return json({ success: false, message: "用户不存在" }, 400);
  }
  if (!verifyPassword(securityAnswer.trim(), user.securityAnswerHash)) {
    return json({ success: false, message: "密保答案错误" }, 400);
  }

  const resetToken = generateToken();
  const store = getStore("basketball-auth");
  await store.set("reset_" + resetToken, JSON.stringify({ userId: user.id, nickname: user.nickname }));

  return json({ success: true, message: "验证成功", resetToken });
}

async function handleResetPassword(body) {
  const { nickname, resetToken, newPassword } = body;
  const store = getStore("basketball-auth");
  const raw = await store.get("reset_" + resetToken);

  if (!raw) {
    return json({ success: false, message: "重置令牌无效或已过期" }, 400);
  }

  const resetData = JSON.parse(raw);
  if (resetData.nickname !== nickname.trim()) {
    return json({ success: false, message: "用户信息不匹配" }, 400);
  }
  if (!newPassword || newPassword.length < 4) {
    return json({ success: false, message: "密码至少需要4个字符" }, 400);
  }

  const users = await getUsers();
  const user = users.find((u) => u.id === resetData.userId);
  if (user) {
    user.passwordHash = hashPassword(newPassword);
    await saveUsers(users);
  }

  await store.delete("reset_" + resetToken);
  return json({ success: true, message: "密码重置成功" });
}

async function handleChangeNickname(request, body) {
  const auth = request.headers.get("authorization") || "";
  const token = auth.startsWith("Bearer ") ? auth.slice(7) : "";
  const sessions = await getSessions();
  const session = getUserByToken(sessions, token);

  if (!session) {
    return json({ success: false, message: "请先登录" }, 401);
  }

  const newName = (body.newNickname || "").trim();
  if (!newName || newName.length > 20) {
    return json({ success: false, message: "昵称不能为空且不超过20个字符" }, 400);
  }

  const users = await getUsers();
  if (users.find((u) => u.nickname === newName)) {
    return json({ success: false, message: "该昵称已被使用" }, 400);
  }

  const user = users.find((u) => u.id === session.userId);
  if (user) {
    user.nickname = newName;
    session.nickname = newName;
    sessions[token] = session;
    await saveUsers(users);
    await saveSessions(sessions);
  }

  return json({ success: true, message: "昵称修改成功" });
}

async function handleMe(request) {
  const auth = request.headers.get("authorization") || "";
  const token = auth.startsWith("Bearer ") ? auth.slice(7) : "";
  const sessions = await getSessions();
  const session = getUserByToken(sessions, token);

  if (!session) {
    return json({ success: false, message: "未登录" }, 401);
  }
  return json({ success: true, user: { id: session.userId, nickname: session.nickname } });
}

// ====== Main Handler ======

export default async function handler(request) {
  if (request.method === "OPTIONS") {
    return json({ status: "ok" });
  }

  const action = parseAction(request.url);
  let body = {};
  if (request.method === "POST") {
    try {
      body = await request.json();
    } catch {
      // no body
    }
  }

  try {
    switch (action) {
      case "security-questions":
        return request.method === "GET"
          ? handleGetSecurityQuestions()
          : json({ error: "Method not allowed" }, 405);
      case "register":
        return handleRegister(body);
      case "login":
        return handleLogin(body);
      case "logout":
        return handleLogout(request);
      case "forgot-password":
        return handleForgotPassword(body);
      case "verify-answer":
        return handleVerifyAnswer(body);
      case "reset-password":
        return handleResetPassword(body);
      case "change-nickname":
        return handleChangeNickname(request, body);
      case "me":
        return request.method === "GET"
          ? handleMe(request)
          : json({ error: "Method not allowed" }, 405);
      default:
        return json({ error: "Unknown action: " + action }, 404);
    }
  } catch (e) {
    return json({ success: false, message: e.message }, 500);
  }
}
