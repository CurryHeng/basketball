import { getStore } from "@netlify/blobs";

const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"];
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "Content-Type, Authorization",
      "Access-Control-Allow-Methods": "GET, POST, DELETE, OPTIONS",
    },
  });
}

function parseAction(rawUrl) {
  const path = new URL(rawUrl).pathname;
  const parts = path.replace(/\/$/, "").split("/");
  return parts[parts.length - 1];
}

async function getUploads() {
  const store = getStore("basketball-uploads");
  const raw = await store.get("uploads");
  return raw ? JSON.parse(raw) : [];
}

async function saveUploads(uploads) {
  const store = getStore("basketball-uploads");
  await store.set("uploads", JSON.stringify(uploads));
}

// ====== Route Handlers ======

async function handleUpload(request) {
  let fileData, fileName, contentType, playerId, uploaderName;

  try {
    const formData = await request.formData();
    const file = formData.get("file");
    playerId = formData.get("playerId");
    uploaderName = (formData.get("uploaderName") || "").trim().slice(0, 20) || "anonymous";

    if (!file) {
      return json({ success: false, message: "未找到上传文件" }, 400);
    }
    if (!playerId) {
      return json({ success: false, message: "缺少球员ID" }, 400);
    }

    contentType = file.type;
    fileName = file.name || "untitled";

    if (!ALLOWED_TYPES.includes(contentType)) {
      return json({ success: false, message: "不支持的文件类型，仅支持 JPG/PNG/GIF/WebP" }, 400);
    }
    if (file.size > MAX_FILE_SIZE) {
      return json({ success: false, message: "文件过大，最大支持 5MB" }, 400);
    }

    const buffer = await file.arrayBuffer();
    fileData = new Uint8Array(buffer);
  } catch (e) {
    return json({ success: false, message: "文件解析失败: " + e.message }, 400);
  }

  const uploads = await getUploads();
  const id = uploads.length > 0 ? Math.max(...uploads.map((u) => u.id)) + 1 : 1;

  const record = {
    id,
    playerId: parseInt(playerId),
    uploaderName,
    fileName,
    contentType,
    size: fileData.length,
    createdAt: new Date().toISOString(),
  };

  const store = getStore("basketball-uploads");
  await store.set("file_" + id, fileData);
  uploads.push(record);
  await saveUploads(uploads);

  return json({ success: true, message: "上传成功", data: record });
}

async function handleList(request) {
  const url = new URL(request.url);
  const playerId = url.searchParams.get("playerId");
  if (!playerId) {
    return json({ success: false, message: "缺少球员ID参数" }, 400);
  }

  const uploads = await getUploads();
  const filtered = uploads
    .filter((u) => u.playerId === parseInt(playerId))
    .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));

  return json({ success: true, data: filtered });
}

async function handleGetFile(request) {
  const url = new URL(request.url);
  const id = url.searchParams.get("id");
  if (!id) {
    return json({ success: false, message: "缺少文件ID参数" }, 400);
  }

  const uploads = await getUploads();
  const record = uploads.find((u) => u.id === parseInt(id));
  if (!record) {
    return json({ success: false, message: "文件不存在" }, 404);
  }

  const store = getStore("basketball-uploads");
  const data = await store.get("file_" + id);
  if (!data) {
    return json({ success: false, message: "文件数据不存在" }, 404);
  }

  return new Response(data, {
    status: 200,
    headers: {
      "Content-Type": record.contentType,
      "Content-Disposition": "inline; filename=\"" + record.fileName + "\"",
      "Cache-Control": "public, max-age=86400",
      "Access-Control-Allow-Origin": "*",
    },
  });
}

async function handleDelete(request) {
  const url = new URL(request.url);
  const id = url.searchParams.get("id");
  if (!id) {
    return json({ success: false, message: "缺少文件ID参数" }, 400);
  }

  const uploads = await getUploads();
  const idx = uploads.findIndex((u) => u.id === parseInt(id));
  if (idx === -1) {
    return json({ success: false, message: "记录不存在" }, 404);
  }

  const store = getStore("basketball-uploads");
  await store.delete("file_" + id);
  uploads.splice(idx, 1);
  await saveUploads(uploads);

  return json({ success: true, message: "删除成功" });
}

// ====== Main Handler ======

export default async function handler(request) {
  if (request.method === "OPTIONS") {
    return json({ status: "ok" });
  }

  const action = parseAction(request.url);

  try {
    switch (action) {
      case "upload":
        return request.method === "POST"
          ? handleUpload(request)
          : json({ error: "Method not allowed" }, 405);
      case "list":
        return request.method === "GET"
          ? handleList(request)
          : json({ error: "Method not allowed" }, 405);
      case "file":
        return request.method === "GET"
          ? handleGetFile(request)
          : json({ error: "Method not allowed" }, 405);
      case "delete":
        return request.method === "DELETE"
          ? handleDelete(request)
          : json({ error: "Method not allowed" }, 405);
      default:
        return json({ error: "Unknown action: " + action }, 404);
    }
  } catch (e) {
    return json({ success: false, message: e.message }, 500);
  }
}
