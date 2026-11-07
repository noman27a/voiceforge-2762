/* VoiceForge 2762 — frontend logic (written from scratch). */
const $ = (id) => document.getElementById(id);
let allVoices = [];
let selectedVoice = "alba";

// ---- tabs ----
document.querySelectorAll("#tabs button").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll("#tabs button").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".tab").forEach((t) => t.classList.remove("active"));
    btn.classList.add("active");
    $("tab-" + btn.dataset.tab).classList.add("active");
    if (btn.dataset.tab === "history") loadHistory();
    if (btn.dataset.tab === "clone") loadCloned();
    if (btn.dataset.tab === "setup") loadSetupStatus();
  });
});

// ---- status ----
async function loadStatus() {
  try {
    const r = await fetch("/api/setup-status");
    const s = await r.json();
    const badge = $("statusBadge");
    if (s.model_loaded) {
      badge.textContent = "✅ Model ready" + (s.voice_cloning ? " · Cloning ON" : "");
      badge.className = "badge ok";
    } else if (s.loading) {
      badge.textContent = "⏳ " + (s.status || "Loading…") + " " + s.progress + "%";
      badge.className = "badge";
      setTimeout(loadStatus, 3000);
    } else {
      badge.textContent = "⚠️ Model not loaded — open Setup";
      badge.className = "badge bad";
      setTimeout(loadStatus, 5000);
    }
  } catch (e) {
    $("statusBadge").textContent = "❌ Server unreachable";
    $("statusBadge").className = "badge bad";
  }
}

// ---- voices ----
async function loadVoices() {
  const r = await fetch("/api/voices");
  const d = await r.json();
  allVoices = d.voices || [];
  const sel = $("voiceSelect");
  const groups = [
    ["⭐ Featured characters", (v) => (v.tags || []).includes("featured")],
    ["Base voices", (v) => !v.is_style && !v.is_cloned],
    ["Deep", (v) => v.is_style && (v.tags || []).includes("deep")],
    ["Warm", (v) => v.is_style && (v.tags || []).includes("warm")],
    ["Bright", (v) => v.is_style && (v.tags || []).includes("bright")],
    ["Energetic", (v) => v.is_style && (v.tags || []).includes("energetic")],
    ["Calm", (v) => v.is_style && (v.tags || []).includes("calm")],
    ["Soft", (v) => v.is_style && (v.tags || []).includes("soft")],
    ["Cloned voices", (v) => !!v.is_cloned],
  ];
  const used = new Set();
  const opt = (v) => `<option value="${v.id}">${v.name} (${v.gender})${v.is_cloned ? " 🧬" : ""}${v.is_style ? " 🎭" : ""}</option>`;
  sel.innerHTML = groups.map(([label, test]) => {
    const items = allVoices.filter((v) => test(v) && !used.has(v.id));
    items.forEach((v) => used.add(v.id));
    return items.length ? `<optgroup label="${label}">${items.map(opt).join("")}</optgroup>` : "";
  }).join("") + allVoices.filter((v) => !used.has(v.id)).map(opt).join("");
  sel.value = selectedVoice;
  renderVoiceGrid();
  loadBgm();
}

function renderVoiceGrid() {
  const q = ($("voiceSearch").value || "").toLowerCase();
  const g = $("genderFilter").value;
  const c = $("categoryFilter").value;
  const list = allVoices.filter((v) => {
    if (g && v.gender !== g) return false;
    if (q && !(v.name + " " + (v.description || "")).toLowerCase().includes(q)) return false;
    if (!c) return true;
    if (c === "base") return !v.is_style && !v.is_cloned;
    if (c === "cloned") return !!v.is_cloned;
    return (v.tags || []).includes(c);
  });
  $("voiceGrid").innerHTML = list.map((v) => `
    <div class="card">
      <h3>${v.name}${v.is_cloned ? " 🧬" : ""}${v.is_style ? " 🎭" : ""}</h3>
      <p>${v.description || ""}</p>
      <div>${(v.tags || []).map((t) => `<span class="tag">${t}</span>`).join("")}</div>
      <button class="btn" onclick="previewVoice('${v.id}')">▶️ Preview</button>
      <button class="btn" onclick="useVoice('${v.id}')">Use in Studio</button>
    </div>`).join("") || "<p>No voices match.</p>";
}

function useVoice(id) {
  selectedVoice = id;
  $("voiceSelect").value = id;
  document.querySelector('[data-tab="studio"]').click();
}

async function previewVoice(id) {
  const url = "/api/preview/" + encodeURIComponent(id);
  const a = new Audio(url);
  a.play().catch(() => alert("Preview failed — model may still be loading."));
}

$("voiceSearch").addEventListener("input", renderVoiceGrid);
$("genderFilter").addEventListener("change", renderVoiceGrid);
$("categoryFilter").addEventListener("change", renderVoiceGrid);
$("voiceSelect").addEventListener("change", (e) => (selectedVoice = e.target.value));

// ---- sliders ----
function bindSlider(inputId, valId, fmt) {
  $(inputId).addEventListener("input", (e) => { $(valId).textContent = fmt(e.target.value); });
}
bindSlider("speedInput", "speedVal", (v) => parseFloat(v).toFixed(2) + "×");
bindSlider("pitchInput", "pitchVal", (v) => parseFloat(v).toFixed(2) + "×");
bindSlider("reverbInput", "reverbVal", (v) => v);

// ---- BGM ----
async function loadBgm() {
  try {
    const r = await fetch("/api/bgm");
    const d = await r.json();
    $("bgmSelect").innerHTML = '<option value="">— None —</option>' +
      (d.bgm_files || []).map((f) => `<option value="${f}">${f}</option>`).join("");
  } catch (e) { /* ignore */ }
}

// ---- generate ----
$("generateBtn").addEventListener("click", async () => {
  const text = $("textInput").value.trim();
  if (!text) { setStatus("genStatus", "Pehle text likho.", true); return; }
  const btn = $("generateBtn");
  btn.disabled = true;
  btn.textContent = "⏳ Generating…";
  setStatus("genStatus", "Voiceover ban raha hai… (pehli dafa model load hone me time lag sakta hai)");
  try {
    const r = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text,
        voice_id: $("voiceSelect").value,
        speed: parseFloat($("speedInput").value),
        pitch: parseFloat($("pitchInput").value),
        reverb: parseFloat($("reverbInput").value),
        bgm_file: $("bgmSelect").value || null,
        output_format: $("formatSelect").value,
      }),
    });
    if (!r.ok) {
      const err = await r.json().catch(() => ({}));
      throw new Error(err.detail || ("HTTP " + r.status));
    }
    const blob = await r.blob();
    const url = URL.createObjectURL(blob);
    const dur = r.headers.get("X-Duration");
    $("player").src = url;
    const dl = $("downloadLink");
    dl.href = url;
    dl.download = "voiceforge2762." + $("formatSelect").value;
    $("playerWrap").hidden = false;
    setStatus("genStatus", "✅ Ready! Duration: " + (dur || "?") + "s — neeche suno ya download karo.", false, true);
  } catch (e) {
    setStatus("genStatus", "❌ Failed: " + e.message, true);
  } finally {
    btn.disabled = false;
    btn.textContent = "🎙️ Generate Voiceover";
  }
});

// ---- clone ----
$("cloneBtn").addEventListener("click", async () => {
  const name = $("cloneName").value.trim();
  const file = $("cloneFile").files[0];
  if (!name) { setStatus("cloneStatus", "Voice ka naam likho.", true); return; }
  if (!file) { setStatus("cloneStatus", "Reference audio file select karo.", true); return; }
  const btn = $("cloneBtn");
  btn.disabled = true;
  btn.textContent = "⏳ Cloning…";
  setStatus("cloneStatus", "Voice clone ho rahi hai…");
  try {
    const fd = new FormData();
    fd.append("audio", file);
    fd.append("name", name);
    const r = await fetch("/api/clone", { method: "POST", body: fd });
    const d = await r.json();
    if (!r.ok) throw new Error(d.detail || "Clone failed");
    setStatus("cloneStatus", "✅ Voice cloned: " + d.voice.name + " — ab Studio me use kar sakte ho!", false, true);
    loadVoices();
    loadCloned();
  } catch (e) {
    setStatus("cloneStatus", "❌ Failed: " + e.message, true);
  } finally {
    btn.disabled = false;
    btn.textContent = "🧬 Clone Voice";
  }
});

async function loadCloned() {
  const r = await fetch("/api/cloned-voices");
  const d = await r.json();
  $("clonedList").innerHTML = (d.voices || []).map((v) => `
    <div class="card"><h3>${v.name} 🧬</h3><p>${v.description || ""}</p>
    <button class="btn" onclick="useVoice('${v.id}')">Use in Studio</button>
    <button class="btn" onclick="deleteCloned('${v.id}')">🗑️ Delete</button></div>`).join("")
    || "<p>No cloned voices yet.</p>";
}

async function deleteCloned(id) {
  if (!confirm("Delete this cloned voice?")) return;
  await fetch("/api/cloned-voices/" + encodeURIComponent(id), { method: "DELETE" });
  loadVoices();
  loadCloned();
}

// ---- batch ----
$("batchBtn").addEventListener("click", async () => {
  const lines = $("batchInput").value.split("\n").map((s) => s.trim()).filter(Boolean);
  if (!lines.length) { setStatus("batchStatus", "Kuch lines likho.", true); return; }
  const btn = $("batchBtn");
  btn.disabled = true;
  btn.textContent = "⏳ Generating batch…";
  setStatus("batchStatus", lines.length + " lines generate ho rahi hain…");
  try {
    const r = await fetch("/api/batch", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        texts: lines,
        voice_id: $("voiceSelect").value,
        speed: parseFloat($("speedInput").value),
        pitch: parseFloat($("pitchInput").value),
        reverb: parseFloat($("reverbInput").value),
        output_format: $("formatSelect").value,
      }),
    });
    if (!r.ok) {
      const err = await r.json().catch(() => ({}));
      throw new Error(err.detail || ("HTTP " + r.status));
    }
    const blob = await r.blob();
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "VoiceForge2762_Batch.zip";
    a.click();
    setStatus("batchStatus", "✅ Batch ZIP download ho gaya!", false, true);
  } catch (e) {
    setStatus("batchStatus", "❌ Failed: " + e.message, true);
  } finally {
    btn.disabled = false;
    btn.textContent = "📦 Generate Batch (ZIP)";
  }
});

// ---- history ----
async function loadHistory() {
  const r = await fetch("/api/history");
  const d = await r.json();
  $("historyList").innerHTML = (d.history || []).map((h) => `
    <div class="history-item">
      <p>${(h.text || "").replace(/</g, "&lt;")}</p>
      <small>Voice: ${h.voice_id} · ${h.duration}s · ${h.format} · ${new Date(h.timestamp * 1000).toLocaleString()}</small><br>
      ${h.has_audio ? `<audio controls src="${h.audio_url}" style="width:100%;margin-top:6px"></audio>
      <a class="btn" href="${h.audio_url}" download>⬇️ Download</a>` : ""}
    </div>`).join("") || "<p>No history yet.</p>";
}
$("refreshHistory").addEventListener("click", loadHistory);

// ---- setup ----
async function loadSetupStatus() {
  const r = await fetch("/api/setup-status");
  const s = await r.json();
  $("setupInfo").textContent = "Status: " + s.status + " (" + s.progress + "%) · Cloning: " + (s.voice_cloning ? "available ✅" : "not available");
  const c = await (await fetch("/api/clone-status")).json();
  $("setupInfo").textContent += " · " + c.message;
}
$("setupStartBtn").addEventListener("click", async () => {
  await fetch("/api/setup-start", { method: "POST" });
  loadSetupStatus();
  loadStatus();
});
$("tokenBtn").addEventListener("click", async () => {
  const token = $("hfToken").value.trim();
  if (!token.startsWith("hf_")) { setStatus("tokenStatus", "Token hf_ se start hona chahiye.", true); return; }
  setStatus("tokenStatus", "Checking token…");
  const r = await fetch("/api/set-token", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token }),
  });
  const d = await r.json();
  if (r.ok) setStatus("tokenStatus", "✅ " + d.message, false, true);
  else setStatus("tokenStatus", "❌ " + (d.detail || "Failed"), true);
  loadSetupStatus();
  loadStatus();
});
$("tokenResetBtn").addEventListener("click", async () => {
  await fetch("/api/reset-token", { method: "POST" });
  setStatus("tokenStatus", "Token reset ho gaya.");
  loadSetupStatus();
});

// ---- helpers ----
function setStatus(id, msg, isErr, isGood) {
  const el = $(id);
  el.textContent = msg;
  el.className = "status" + (isErr ? " err" : isGood ? " good" : "");
}

// ---- init ----
loadStatus();
loadVoices();
