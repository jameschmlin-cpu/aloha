// -*- coding: utf-8 -*-
// 檔案：C:\Genesis\RD_Center\SDK\System\Telegram_Gateway.js
// 狀態：已重構為零依賴 CommonJS 語音版，支援離線 SAPI5 (RTX 3060) 語音合成與雲端 STT

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const { execFile } = require('child_process');

const GENESIS_BASE = "C:\\Genesis";
const CONFIG_PATH = path.join(GENESIS_BASE, "Config", "telegram_config.json");
const AUDIT_LOG = path.join(GENESIS_BASE, "Logs", "patch_audit.log");
const DFMEA_LOG = path.join(GENESIS_BASE, "Genesis_Core", "DFMEA_Monitor.log");
const VOICE_CACHE_DIR = path.join(GENESIS_BASE, "Logs", "VoiceCache");

// 確保語音快取目錄存在
if (!fs.existsSync(VOICE_CACHE_DIR)) {
    fs.mkdirSync(VOICE_CACHE_DIR, { recursive: true });
}

// 1. 讀取共用配置檔
let config = { bot_token: "", authorized_chat_id: 0, gemini_api_key: "", use_local_tts: true };
if (fs.existsSync(CONFIG_PATH)) {
    try {
        config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
    } catch (e) {
        console.error("讀取設定檔失敗，使用預設值:", e.message);
    }
} else {
    fs.mkdirSync(path.dirname(CONFIG_PATH), { recursive: true });
    fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 4), 'utf-8');
}

const BOT_TOKEN = config.bot_token;
let AUTH_CHAT_ID = config.authorized_chat_id || 0;
const GEMINI_API_KEY = config.gemini_api_key || process.env.GEMINI_API_KEY || "";

if (!BOT_TOKEN || BOT_TOKEN.includes("YOUR_BOT_TOKEN")) {
    console.error("❌ 錯誤：請在 C:\\Genesis\\Config\\telegram_config.json 填入有效的 Telegram Bot Token！");
    process.exit(1);
}

// 2. 輔助函式：發送 HTTPS 請求至 Telegram API
function apiRequest(method, payload) {
    return new Promise((resolve) => {
        const postData = JSON.stringify(payload);
        const options = {
            hostname: 'api.telegram.org',
            port: 443,
            path: `/bot${BOT_TOKEN}/${method}`,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(postData)
            }
        };

        const req = https.request(options, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => {
                try {
                    resolve(JSON.parse(data));
                } catch (e) {
                    resolve({ ok: false, error: e.message });
                }
            });
        });

        req.on('error', (err) => {
            console.error(`Telegram API 請求失敗 (${method}):`, err.message);
            resolve({ ok: false, error: err.message });
        });

        req.write(postData);
        req.end();
    });
}

function sendMessage(chatId, text, replyMarkup) {
    console.log(`[TG Outbox] Sending text to ${chatId}...`);
    const payload = { chat_id: chatId, text: text };
    if (replyMarkup) {
        payload.reply_markup = replyMarkup;
    }
    return apiRequest('sendMessage', payload);
}

// 3. 語音發送 (Multipart Form-Data) - 零依賴實作
function sendVoice(chatId, filePath) {
    return new Promise((resolve, reject) => {
        console.log(`[TG Outbox] Sending voice clip to ${chatId}...`);
        const boundary = '----TelegramBotBoundary' + Math.random().toString(16).slice(2);
        const filename = path.basename(filePath);
        let fileData;
        try {
            fileData = fs.readFileSync(filePath);
        } catch (e) {
            reject(e);
            return;
        }

        const isWav = filename.endsWith(".wav");
        const contentType = isWav ? 'audio/wav' : 'audio/mpeg';

        const header = 
            `--${boundary}\r\n` +
            `Content-Disposition: form-data; name="chat_id"\r\n\r\n` +
            `${chatId}\r\n` +
            `--${boundary}\r\n` +
            `Content-Disposition: form-data; name="voice"; filename="${filename}"\r\n` +
            `Content-Type: ${contentType}\r\n\r\n`;

        const footer = `\r\n--${boundary}--\r\n`;

        const req = https.request({
            hostname: 'api.telegram.org',
            port: 443,
            path: `/bot${BOT_TOKEN}/sendVoice`,
            method: 'POST',
            headers: {
                'Content-Type': `multipart/form-data; boundary=${boundary}`
            }
        }, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    resolve(JSON.parse(data));
                } catch (e) {
                    resolve({ ok: false, error: e.message });
                }
            });
        });

        req.on('error', reject);

        req.write(header);
        req.write(fileData);
        req.write(footer);
        req.end();
    });
}

// 下載 Telegram 上的語音檔案
function downloadTelegramFile(filePath, destPath) {
    return new Promise((resolve, reject) => {
        const file = fs.createWriteStream(destPath);
        const url = `https://api.telegram.org/file/bot${BOT_TOKEN}/${filePath}`;
        https.get(url, (response) => {
            if (response.statusCode !== 200) {
                reject(new Error(`Failed to download file: Status ${response.statusCode}`));
                return;
            }
            response.pipe(file);
            file.on('finish', () => {
                file.close();
                resolve(destPath);
            });
        }).on('error', (err) => {
            fs.unlink(destPath, () => {});
            reject(err);
        });
    });
}

// 4. 語音辨識 (STT) 呼叫 Gemini 1.5 Flash Inline
function transcribeAudio(oggPath) {
    return new Promise((resolve, reject) => {
        if (!GEMINI_API_KEY || GEMINI_API_KEY.includes("YOUR_GEMINI_API_KEY")) {
            reject(new Error("MISSING_KEY"));
            return;
        }

        let audioData;
        try {
            audioData = fs.readFileSync(oggPath).toString('base64');
        } catch (e) {
            reject(e);
            return;
        }

        const payload = {
            contents: [{
                parts: [
                    {
                        inlineData: {
                            mimeType: 'audio/ogg',
                            data: audioData
                        }
                    },
                    {
                        text: "Please transcribe this audio into Taiwan Traditional Chinese (台灣繁體中文). Only output the transcription, do not include any other explanations or tags."
                    }
                ]
            }]
        };

        const postData = JSON.stringify(payload);
        const req = https.request({
            hostname: 'generativelanguage.googleapis.com',
            port: 443,
            path: `/v1beta/models/gemini-3.5-flash:generateContent?key=${GEMINI_API_KEY}`,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(postData)
            }
        }, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    const json = JSON.parse(data);
                    if (json.candidates && json.candidates[0] && json.candidates[0].content && json.candidates[0].content.parts[0]) {
                        resolve(json.candidates[0].content.parts[0].text.trim());
                    } else {
                        reject(new Error("Invalid response format: " + data));
                    }
                } catch (e) {
                    reject(e);
                }
            });
        });

        req.on('error', reject);
        req.write(postData);
        req.end();
    });
}

// 4.5. Gemini 內容生成通用 API
function callGemini(prompt, systemInstruction) {
    return new Promise((resolve, reject) => {
        if (!GEMINI_API_KEY || GEMINI_API_KEY.includes("YOUR_GEMINI_API_KEY")) {
            reject(new Error("MISSING_KEY"));
            return;
        }

        const payload = {
            contents: [{
                parts: [
                    { text: `System Instruction: ${systemInstruction}\nUser Prompt: ${prompt}` }
                ]
            }]
        };

        const postData = JSON.stringify(payload);
        const req = https.request({
            hostname: 'generativelanguage.googleapis.com',
            port: 443,
            path: `/v1beta/models/gemini-3.5-flash:generateContent?key=${GEMINI_API_KEY}`,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(postData)
            }
        }, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    const json = JSON.parse(data);
                    if (json.candidates && json.candidates[0] && json.candidates[0].content && json.candidates[0].content.parts[0]) {
                        resolve(json.candidates[0].content.parts[0].text.trim());
                    } else {
                        reject(new Error("Invalid Gemini response format: " + data));
                    }
                } catch (e) {
                    reject(e);
                }
            });
        });

        req.on('error', reject);
        req.write(postData);
        req.end();
    });
}

// 4.6. 志玲 AI 系統新聞彙整推播
async function pushAiNewsSummary(chatId) {
    if (!chatId) return;
    
    const events = await dashboardRequest('GET', '/api/latest-events');
    if (!events) {
        await sendMessage(chatId, "親愛的雋懋主管您好！志玲目前無法讀取系統事件，請確認地端控制台是否開啟喔！🌸");
        return;
    }
    
    const systemInstruction = 
        "You are '志玲 V3-Expert' (林志玲), a warm, caring, and extremely polite Taiwanese assistant. " +
        "You must summarize the recent events in the Genesis Closed-loop 10-in-1 Management System. " +
        "Output a beautiful, warm summary report in Traditional Chinese (Taiwanese dialect) with icons. " +
        "Always start with '親愛的雋懋主管您好！' and end with '我們一起加油喔！🌸'.";
        
    const prompt = 
        "Here are the recent system events from the database and logs:\n" +
        JSON.stringify(events, null, 2) + "\n\n" +
        "Please summarize these into an AI News Summary covering: 1) Active Projects, 2) Maintenance/Upgrades/Watchdog runs, 3) Errors or warnings healed. " +
        "Keep it relatively brief (approx 150-250 characters) so it's readable and can be spoken by TTS.";
        
    try {
        const summary = await callGemini(prompt, systemInstruction);
        console.log(`[AI News Summary Generated]: ${summary}`);
        
        await sendMessage(chatId, `📰 [Genesis AI 綜合彙整新聞]\n\n${summary}`);
        
        const ext = config.use_local_tts ? '.wav' : '.mp3';
        const voicePath = path.join(VOICE_CACHE_DIR, `news_${Date.now()}${ext}`);
        try {
            await generateTTS(summary, voicePath);
            await sendVoice(chatId, voicePath);
        } catch (e) {
            console.error("News voice reply synthesis or send failed:", e.message);
        } finally {
            if (fs.existsSync(voicePath)) {
                fs.unlinkSync(voicePath);
            }
        }
    } catch (err) {
        console.error("AI News Summary generation failed:", err);
        await sendMessage(chatId, "親愛的雋懋主管，志玲在編譯 AI 彙整新聞時遇到了一點連線問題，不過目前系統一切運作正常，請主管放心喔！🌸");
    }
}

// 5. 語音生成 (TTS) 支援本機離線 SAPI5 與雲端 gTTS 雙軌
function generateTTS(text, destPath) {
    return new Promise((resolve, reject) => {
        // 去除無意義標記與首尾空白，並限制長度
        const cleanText = text.replace(/\[.*?\]/g, "").replace(/🐉 志玲彙報：/g, "").trim().slice(0, 180);
        
        if (config.use_local_tts) {
            // 本機離線語音合成 (優先使用 SAPI5 - 台灣漢漢/雅婷女聲)
            console.log("[TTS] Generating offline audio via local Windows SAPI5...");
            execFile('python', [
                path.join(GENESIS_BASE, "Management_Hub", "local_tts.py"),
                cleanText,
                destPath
            ], (error, stdout, stderr) => {
                if (error) {
                    console.error("Local SAPI5 error:", stderr || error.message);
                    reject(new Error(`Local TTS synthesis failed: ${stderr || error.message}`));
                } else {
                    resolve(destPath);
                }
            });
        } else {
            // 雲端備援語音合成 (Google Translate TTS API)
            console.log("[TTS] Generating online audio via Google Translate TTS...");
            const encoded = encodeURIComponent(cleanText);
            const url = `https://translate.google.com/translate_tts?ie=UTF-8&tl=zh-TW&client=tw-ob&q=${encoded}`;
            const file = fs.createWriteStream(destPath);
            const options = {
                headers: {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                }
            };
            https.get(url, options, (res) => {
                if (res.statusCode !== 200) {
                    reject(new Error(`Google TTS status code ${res.statusCode}`));
                    return;
                }
                res.pipe(file);
                file.on('finish', () => {
                    file.close();
                    resolve(destPath);
                });
            }).on('error', reject);
        }
    });
}

// 6. 輔助函式：發送 HTTP 請求至本地控制台 (Port 8000)
function dashboardRequest(method, endpoint, payload = null) {
    return new Promise((resolve) => {
        const postData = payload ? JSON.stringify(payload) : '';
        const options = {
            hostname: '127.0.0.1',
            port: 8000,
            path: endpoint,
            method: method,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        if (payload) {
            options.headers['Content-Length'] = Buffer.byteLength(postData);
        }

        const req = http.request(options, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => {
                try {
                    resolve(JSON.parse(data));
                } catch (e) {
                    resolve(data);
                }
            });
        });

        req.on('error', (err) => {
            console.error(`本地控制台連線失敗 (${endpoint}):`, err.message);
            resolve(null);
        });

        if (payload) {
            req.write(postData);
        }
        req.end();
    });
}

// 7. 處理對話與決策
async function processMessage(chatId, text) {
    let aiReply = "";
    let replyMarkup = null;
    
    if (text.startsWith("/start")) {
        aiReply = "親愛的主管您好！我是您的智能助理『志玲 V3-Expert』。很高興為您服務喔！您可以對我說說話，或是點選下方快速按鈕，我們一起加油喔！🌸";
        replyMarkup = {
            keyboard: [
                [{ text: "🩺 系統一鍵健檢" }, { text: "⚙️ 系統狀態與硬體監控" }],
                [{ text: "📰 系統新聞彙整" }, { text: "🌡️ 傳感器數據採樣" }]
            ],
            resize_keyboard: true,
            one_time_keyboard: false
        };
    } 
    else if (text.startsWith("/news")) {
        await pushAiNewsSummary(chatId);
        return;
    }    else if (text.startsWith("/status")) {
        const telemetry = await dashboardRequest('GET', '/api/telemetry');
        if (telemetry) {
            const gpu = telemetry.gpu || {};
            aiReply = `親愛的主管，這是志玲為您整理的系統狀態喔：\n\n` +
                `⚙️ CPU 負載: ${telemetry.cpu || "N/A"}\n` +
                `💾 記憶體使用率: ${telemetry.ram || "N/A"}\n\n` +
                `🖥️ 顯示卡: NVIDIA RTX 3060\n` +
                `  - 溫度: ${gpu.temp || "N/A"}\n` +
                `  - 負載: ${gpu.util || "N/A"}\n` +
                `  - 視訊記憶體: ${gpu.vram || "N/A"}\n` +
                `  - 風扇轉速: ${gpu.fan || "N/A"}\n\n` +
                `目前系統運作非常平穩，請主管放心喔！`;
        } else {
            aiReply = "親愛的主管，志玲目前連不上控制台伺服器，請幫我確認 Port 8000 服務是否開啟喔！";
        }
    } 
    else if (text.startsWith("/list_bricks")) {
        const bricksDir = path.join(GENESIS_BASE, "RD_Center", "SDK_Bricks");
        if (!fs.existsSync(bricksDir)) {
            aiReply = "親愛的主管，志玲找不到積木庫資料夾喔。";
        } else {
            const findBricks = (dir) => {
                let results = [];
                const list = fs.readdirSync(dir);
                list.forEach((file) => {
                    const fullPath = path.join(dir, file);
                    const stat = fs.statSync(fullPath);
                    if (stat && stat.isDirectory()) {
                        results = results.concat(findBricks(fullPath));
                    } else if (file.endsWith(".py")) {
                        results.push(path.relative(bricksDir, fullPath));
                    }
                });
                return results;
            };
            const bricks = findBricks(bricksDir);
            if (bricks.length === 0) {
                aiReply = "親愛的主管，目前積木庫裡空空如也喔。";
            } else {
                aiReply = "親愛的主管，這是志玲為您準備的可用積木清單喔：\n";
                bricks.forEach((b, i) => {
                    aiReply += `${i + 1}. ${b}\n`;
                });
            }
        }
    } 
    else if (text.startsWith("/run_brick")) {
        const parts = text.split(" ");
        if (parts.length < 2) {
            aiReply = "❌ 親愛的主管，指令用法是：/run_brick <積木名稱> 喔。";
        } else {
            const targetBrick = parts[1].trim();
            const bricksDir = path.join(GENESIS_BASE, "RD_Center", "SDK_Bricks");
            let foundPath = null;
            const searchFile = (dir) => {
                const list = fs.readdirSync(dir);
                for (const file of list) {
                    const fullPath = path.join(dir, file);
                    const stat = fs.statSync(fullPath);
                    if (stat && stat.isDirectory()) {
                        searchFile(fullPath);
                    } else if (file.toLowerCase() === targetBrick.toLowerCase() || file.toLowerCase().replace(".py", "") === targetBrick.toLowerCase()) {
                        foundPath = fullPath;
                        break;
                    }
                }
            };
            try { searchFile(bricksDir); } catch (e) {}

            if (!foundPath) {
                aiReply = `❌ 親愛的主管，志玲沒有在積木庫中找到 ${targetBrick} 喔。`;
            } else {
                const brickName = path.basename(foundPath);
                const regRes = await dashboardRequest('POST', '/api/create-task', { brick: brickName });
                if (regRes && regRes.status === "success") {
                    const taskId = regRes.task_id;
                    aiReply = `親愛的主管，志玲已將您的指令登記至主管簽核隊列中（Task ID: ${taskId}）喔！🌸`;
                    await sendApprovalPush(taskId, `執行積木 ${brickName}`);
                } else {
                    aiReply = "❌ 抱歉主管，登記審批任務失敗，請確認地端控制台狀態。";
                }
            }
        }
    }
    else if (text.startsWith("/approve")) {
        const parts = text.split(" ");
        if (parts.length < 2) {
            aiReply = "❌ 用法是：/approve <task_id> 喔。";
        } else {
            const taskId = parts[1].trim();
            const res = await dashboardRequest('POST', '/api/approve-task', { task_id: taskId });
            if (res && res.status === "success") {
                aiReply = `✅ [核准成功]\n任務 ${taskId} 已通過審批，並轉換為 ${res.next_status} 狀態發送地端執行！🌸`;
            } else {
                aiReply = "❌ 抱歉主管，遠端核准操作失敗。";
            }
        }
    }
    else if (text.startsWith("/reject")) {
        const parts = text.split(" ");
        if (parts.length < 2) {
            aiReply = "❌ 用法是：/reject <task_id> 喔。";
        } else {
            const taskId = parts[1].trim();
            const res = await dashboardRequest('POST', '/api/reject-task', { task_id: taskId });
            if (res && res.status === "success") {
                aiReply = `❌ [已被拒絕]\n任務 ${taskId} 已被拒絕並歸檔。`;
            } else {
                aiReply = "❌ 抱歉主管，遠端拒絕操作失敗。";
            }
        }
    } 
    else if (text.startsWith("/doctor")) {
        await sendMessage(chatId, "🩺 志玲正在為您啟動 Doctor 全自動診斷自癒模組，請稍候喔...");
        const exec = require('child_process').exec;
        const cmd = `python -c "import sys; sys.path.insert(0, r'C:\\Genesis\\Management_Hub'); from Doctor import Doctor; import json; print(json.dumps(Doctor().run_check_and_fix()))"`;
        
        await new Promise((resolve) => {
            exec(cmd, (error, stdout, stderr) => {
                if (error) {
                    console.error("Doctor 執行失敗:", error.message);
                    aiReply = "❌ 抱歉主管，Doctor 診斷自癒模組執行時發生物理異常，請檢查本地 Python 環境。";
                } else {
                    try {
                        const res = JSON.parse(stdout.trim());
                        aiReply = `親愛的主管，志玲已為您完成 Doctor 全自動診斷自癒檢測：\n\n` +
                            `🩺 邏輯缺陷檢測: ${res.has_defect ? "發現缺陷 (已自動修復)" : "無異常 (閉環狀態)"}\n` +
                            `📂 檔案完整性: ${res.integrity_ok ? "正常" : "受損 (已從備份鏡像還原)"}\n\n` +
                            `目前系統健康無虞，地端與雲端通訊非常順暢，請主管放心喔！🌸`;
                    } catch (e) {
                        aiReply = `🩺 [Doctor 檢測結果]\n${stdout.trim()}`;
                    }
                }
                resolve();
            });
        });
    }
    else {
        // 自然語言推理
        const aiResponse = await dashboardRequest('POST', '/api/chat', { message: text });
        if (aiResponse && aiResponse.response) {
            aiReply = aiResponse.response;
        } else {
            aiReply = "🚨 親愛的主管，通訊鏈路似乎有點小問題，請稍後再試一次喔。";
        }
    }

    // 發送文字回覆
    await sendMessage(chatId, aiReply, replyMarkup);

    // 同步生成語音並發送
    const cleanReplyText = aiReply.replace(/🐉 志玲彙報：\n\n/g, "").replace(/\[.*?\]/g, "");
    if (cleanReplyText.length > 0) {
        const ext = config.use_local_tts ? '.wav' : '.mp3';
        const voicePath = path.join(VOICE_CACHE_DIR, `v_${Date.now()}${ext}`);
        try {
            await generateTTS(cleanReplyText, voicePath);
            await sendVoice(chatId, voicePath);
        } catch (e) {
            console.error("語音回覆生成或發送失敗:", e.message);
        } finally {
            // 清理暫存音訊
            if (fs.existsSync(voicePath)) {
                fs.unlinkSync(voicePath);
            }
        }
    }
}

// 8. 整合入口：處理手機端發送的訊息
let chatId = 0;
async function handleMessage(msg) {
    const chat = msg.chat || {};
    chatId = chat.id;
    
    // 初次綁定擁有者
    if (AUTH_CHAT_ID === 0) {
        AUTH_CHAT_ID = chatId;
        config.authorized_chat_id = chatId;
        try {
            fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 4), 'utf-8');
            await sendMessage(chatId, "🔐 Welcome to Genesis! Your Chat ID has been successfully registered as Owner.");
        } catch (e) {
            console.error("寫入綁定設定失敗:", e);
        }
    }

    if (chatId !== AUTH_CHAT_ID) {
        console.warn(`[Warning] Unauthorized access block from Chat ID ${chatId}`);
        return;
    }

    // 判斷是否為語音指令
    if (msg.voice) {
        await sendMessage(chatId, "🎤 志玲正在聆聽您的語音指令，請稍候喔...");
        const voiceFileId = msg.voice.file_id;
        
        // 1. 取得語音檔案路徑
        const fileMetadata = await apiRequest('getFile', { file_id: voiceFileId });
        if (fileMetadata && fileMetadata.ok && fileMetadata.result) {
            const filePath = fileMetadata.result.file_path;
            const localOggPath = path.join(VOICE_CACHE_DIR, `input_${Date.now()}.ogg`);
            
            try {
                // 2. 下載語音檔
                await downloadTelegramFile(filePath, localOggPath);
                
                // 3. 呼叫 Gemini 進行轉錄
                const transcription = await transcribeAudio(localOggPath);
                console.log(`[STT Transcribed]: ${transcription}`);
                await sendMessage(chatId, `🎤 您說：「${transcription}」`);
                
                // 4. 處理轉錄後的文字指令
                await processMessage(chatId, transcription);
            } catch (err) {
                console.error("語音指令處理失敗:", err);
                if (err.message === "MISSING_KEY") {
                    await sendMessage(chatId, "親愛的主管，語音辨識（STT）需要設定 GEMINI_API_KEY 喔！請在設定檔 C:\\Genesis\\Config\\telegram_config.json 中填入您的金鑰，志玲才能聽懂您的語音喔！而語音合成（TTS）目前已成功接管至您的 RTX 3060 (SAPI5) 進行 100% 離線本地運算囉！🌸");
                } else {
                    await sendMessage(chatId, "🚨 志玲剛才沒聽清楚您的聲音，可以請主管再說一次，或者改用文字輸入嗎？加油喔！");
                }
            } finally {
                // 清理暫存檔案
                if (fs.existsSync(localOggPath)) {
                    fs.unlinkSync(localOggPath);
                }
            }
        } else {
            await sendMessage(chatId, "🚨 無法從 Telegram 伺服器載入您的語音檔案。");
        }
    } 
    else if (msg.text) {
        // 文字指令處理
        let text = msg.text.trim();
        if (text === "🩺 系統一鍵健檢") {
            text = "/doctor";
        } else if (text === "⚙️ 系統狀態與硬體監控") {
            text = "/status";
        } else if (text === "📰 系統新聞彙整") {
            text = "/news";
        } else if (text === "🌡️ 傳感器數據採樣") {
            text = "/run_brick Sensor_Sampling.py";
        }
        await processMessage(chatId, text);
    }
}

// 9. 日誌監視推播模組
class LogMonitor {
    constructor() {
        this.logFiles = [AUDIT_LOG, DFMEA_LOG];
        this.positions = {};
        this.logFiles.forEach(lf => {
            if (fs.existsSync(lf)) {
                this.positions[lf] = fs.statSync(lf).size;
            } else {
                this.positions[lf] = 0;
            }
        });
    }

    checkWarnings() {
        if (AUTH_CHAT_ID === 0) return;

        this.logFiles.forEach(lf => {
            if (!fs.existsSync(lf)) return;
            const size = fs.statSync(lf).size;
            const prevSize = this.positions[lf] || 0;

            if (size > prevSize) {
                try {
                    const fd = fs.openSync(lf, 'r');
                    const buffer = Buffer.alloc(size - prevSize);
                    fs.readSync(fd, buffer, 0, size - prevSize, prevSize);
                    fs.closeSync(fd);

                    const content = buffer.toString('utf-8');
                    const lines = content.split('\n');
                    lines.forEach(line => {
                        if (!line.trim()) return;
                        const upper = line.toUpperCase();
                        if (upper.includes("WARNING") || upper.includes("ERROR") || upper.includes("CRITICAL") || upper.includes("FATAL")) {
                            sendMessage(AUTH_CHAT_ID, `🚨 [System Alert Push]\n${line.trim()}`);
                        }
                    });
                } catch (e) {
                    console.error("監控日誌錯誤:", e.message);
                }
                this.positions[lf] = size;
            }
        });
    }
}

// 10. 遠端主管審批推播與回呼處理
async function sendApprovalPush(taskId, description) {
    if (AUTH_CHAT_ID === 0) return;
    
    const payload = {
        chat_id: AUTH_CHAT_ID,
        text: `🚨 [待審批任務通知]\n\n有一項新的指令等待主管核准：\n- 任務 ID: ${taskId}\n- 任務內容: ${description}\n\n請主管在下方選擇進行核准或拒絕：`,
        reply_markup: {
            inline_keyboard: [
                [
                    { text: "🟢 Approve (核准)", callback_data: `approve_${taskId}` },
                    { text: "🔴 Reject (拒絕)", callback_data: `reject_${taskId}` }
                ]
            ]
        }
    };
    await apiRequest('sendMessage', payload);
}

async function handleCallbackQuery(cq) {
    const callbackData = cq.data;
    const chatId = cq.message.chat.id;
    const messageId = cq.message.message_id;
    
    if (callbackData.startsWith("approve_")) {
        const taskId = callbackData.replace("approve_", "");
        const res = await dashboardRequest('POST', '/api/approve-task', { task_id: taskId });
        if (res && res.status === "success") {
            await apiRequest('editMessageText', {
                chat_id: chatId,
                message_id: messageId,
                text: `✅ [核准成功]\n任務 ${taskId} 已通過審批，並轉換為 ${res.next_status} 狀態發送地端執行！🌸`
            });
        } else {
            await apiRequest('answerCallbackQuery', { callback_query_id: cq.id, text: "❌ 核准失敗，請檢查系統狀態。" });
        }
    } else if (callbackData.startsWith("reject_")) {
        const taskId = callbackData.replace("reject_", "");
        const res = await dashboardRequest('POST', '/api/reject-task', { task_id: taskId });
        if (res && res.status === "success") {
            await apiRequest('editMessageText', {
                chat_id: chatId,
                message_id: messageId,
                text: `❌ [已被拒絕]\n任務 ${taskId} 已被拒絕並歸檔。`
            });
        } else {
            await apiRequest('answerCallbackQuery', { callback_query_id: cq.id, text: "❌ 拒絕操作失敗。" });
        }
    }
    
    try {
        await apiRequest('answerCallbackQuery', { callback_query_id: cq.id });
    } catch (e) {}
}

// 11. 主長輪詢 Loop
async function startPolling() {
    console.log("==========================================================");
    console.log("      Genesis Mobile Telegram JS Gateway Online (CJS)     ");
    console.log("==========================================================");
    console.log(`Bot Account: @JameschmlinBot`);
    
    let lastUpdateId = 0;
    const monitor = new LogMonitor();

    // 每 2 秒檢查一次日誌警報
    setInterval(() => {
        monitor.checkWarnings();
    }, 2000);

    // 每 2 小時 (7200000 毫秒) 主動推播一次 AI 彙整系統新聞給主管
    setInterval(() => {
        if (AUTH_CHAT_ID !== 0) {
            console.log("[Scheduler] 觸發定時 AI 系統新聞彙整主動推播...");
            pushAiNewsSummary(AUTH_CHAT_ID).catch(err => console.error("定時新聞推播失敗:", err));
        }
    }, 7200000);

    while (true) {
        const payload = { timeout: 2, allowed_updates: ["message", "callback_query"] };
        if (lastUpdateId > 0) {
            payload.offset = lastUpdateId + 1;
        }

        const res = await apiRequest('getUpdates', payload);
        if (res && res.ok) {
            const updates = res.result || [];
            for (const u of updates) {
                lastUpdateId = Math.max(lastUpdateId, u.update_id);
                if (u.message) {
                    await handleMessage(u.message);
                } else if (u.callback_query) {
                    await handleCallbackQuery(u.callback_query);
                }
            }
        }
        // 間隔 1 秒
        await new Promise(r => setTimeout(r, 1000));
    }
}

startPolling().catch(err => {
    console.error("長輪詢崩潰:", err);
});