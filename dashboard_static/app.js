// app.js

document.addEventListener("DOMContentLoaded", () => {
    // DOM Elements
    const fileTreeRoot = document.getElementById("file-tree-root");
    const deviceTreeRoot = document.getElementById("device-tree-root");
    const codeContent = document.getElementById("code-content");
    const projectorFileName = document.getElementById("projector-file-name");
    const btnRunBrick = document.getElementById("btn-run-brick");
    let activeProjectedFilePath = null;
    
    // Header telemetry elements
    const headerCpu = document.getElementById("header-cpu");
    const headerRam = document.getElementById("header-ram");
    const headerGpuTemp = document.getElementById("header-gpu-temp");

    // Chat elements
    const chatMessages = document.getElementById("chat-messages");
    const chatInput = document.getElementById("chat-input");
    const btnSend = document.getElementById("btn-send");
    const tgAgentName = document.getElementById("tg-agent-name");
    const tgAgentStatus = document.getElementById("tg-agent-status");

    // Modal elements: Devices
    const deviceModal = document.getElementById("device-modal");
    const btnOpenModal = document.getElementById("btn-open-modal");
    const btnCloseModal = document.getElementById("btn-close-modal");
    const addDeviceForm = document.getElementById("add-device-form");

    // Modal elements: DFMEA Rules
    const ruleModal = document.getElementById("rule-modal");
    const btnOpenRuleModal = document.getElementById("btn-open-rule-modal");
    const btnCloseRuleModal = document.getElementById("btn-close-rule-modal");
    const addRuleForm = document.getElementById("add-rule-form");
    const ruleModalTitle = document.getElementById("rule-modal-title");
    const ruleActionMode = document.getElementById("rule-action-mode");
    const ruleIdInput = document.getElementById("rule-id");

    // Tab buttons
    const tabButtons = document.querySelectorAll(".tab-btn");
    const tabContents = document.querySelectorAll(".tab-content");

    // Switch Tabs
    tabButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            tabButtons.forEach(b => b.classList.remove("active"));
            tabContents.forEach(c => c.classList.remove("active"));
            
            btn.classList.add("active");
            const targetContent = document.getElementById(`tab-${btn.dataset.tab}`);
            if (targetContent) {
                targetContent.classList.add("active");
                // Force iframe cache-busting reload for ClawLibrary when clicked
                if (btn.dataset.tab === "clawlibrary") {
                    const iframe = targetContent.querySelector("iframe");
                    if (iframe) {
                        iframe.src = "http://" + window.location.hostname + ":5188/?t=" + Date.now();
                    }
                } else if (btn.dataset.tab === "nodered") {
                    const iframe = targetContent.querySelector("iframe");
                    if (iframe) {
                        iframe.src = "http://" + window.location.hostname + ":1880/ui/";
                    }
                }
            }
        });
    });

    // Device Modal controls
    btnOpenModal.addEventListener("click", () => deviceModal.classList.add("active"));
    btnCloseModal.addEventListener("click", () => deviceModal.classList.remove("active"));
    deviceModal.addEventListener("click", (e) => {
        if (e.target === deviceModal) deviceModal.classList.remove("active");
    });

    // DFMEA Rule Modal controls
    btnOpenRuleModal.addEventListener("click", () => {
        ruleModalTitle.innerText = "Add DFMEA Rule";
        ruleActionMode.value = "add";
        ruleIdInput.disabled = false;
        addRuleForm.reset();
        document.getElementById("rule-occurrence").value = 1;
        document.getElementById("rule-detection").value = 1;
        ruleModal.classList.add("active");
    });
    btnCloseRuleModal.addEventListener("click", () => ruleModal.classList.remove("active"));
    ruleModal.addEventListener("click", (e) => {
        if (e.target === ruleModal) ruleModal.classList.remove("active");
    });

    // Form Submission: Add Device
    addDeviceForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const name = document.getElementById("device-name").value;
        const type = document.getElementById("device-type").value;
        const metricName = document.getElementById("metric-label").value;
        const metricValue = document.getElementById("metric-value").value;

        const payload = {
            name: name,
            type: type,
            metrics: {
                [metricName]: metricValue,
                "Status": "ONLINE"
            }
        };

        try {
            const res = await fetch("/api/add-device", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const result = await res.json();
            if (result.status === "success") {
                addLogLine("success", `[DEVICE] Successfully mounted external hardware node: ${name}`);
                deviceModal.classList.remove("active");
                addDeviceForm.reset();
                fetchTree(); 
            }
        } catch (err) {
            alert("Failed to add device node: " + err);
        }
    });

    // Form Submission: Add/Edit Rule
    addRuleForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const payload = {
            id: document.getElementById("rule-id").value,
            problem_point: document.getElementById("rule-problem").value,
            failure_mode: document.getElementById("rule-mode").value,
            severity: parseInt(document.getElementById("rule-severity").value),
            occurrence: parseInt(document.getElementById("rule-occurrence").value || 1),
            detection: parseInt(document.getElementById("rule-detection").value || 1),
            root_cause: document.getElementById("rule-cause").value,
            prevention: document.getElementById("rule-prevention").value,
            corrective: document.getElementById("rule-corrective").value
        };

        try {
            const res = await fetch("/api/dfmea", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const result = await res.json();
            if (result.status === "success") {
                addLogLine("success", `[DFMEA] Saved rule successfully: ${payload.id}`);
                ruleModal.classList.remove("active");
                addRuleForm.reset();
                fetchDFMEA(); 
            }
        } catch (err) {
            alert("Failed to save rule: " + err);
        }
    });

    // Add log helper
    const consoleLogs = document.getElementById("console-logs");
    function addLogLine(type, message) {
        const time = new Date().toLocaleTimeString();
        const line = document.createElement("div");
        line.className = `log-line ${type}`;
        line.innerText = `[${type.toUpperCase()}] [${time}] ${message}`;
        consoleLogs.appendChild(line);
        consoleLogs.scrollTop = consoleLogs.scrollHeight;
    }

    // Render File Tree Node
    function renderFileNode(node) {
        const wrapper = document.createElement("div");
        wrapper.className = "tree-node";

        const item = document.createElement("div");
        item.className = "tree-item";
        item.innerText = (node.isDir ? "📂 " : "📄 ") + node.name;

        if (node.isDir) {
            item.classList.add("folder-node");
            const childrenContainer = document.createElement("div");
            childrenContainer.className = "tree-children";

            item.addEventListener("click", (e) => {
                e.stopPropagation();
                item.classList.toggle("expanded");
                childrenContainer.classList.toggle("active");
            });

            if (node.children && node.children.length > 0) {
                node.children.forEach(child => {
                    childrenContainer.appendChild(renderFileNode(child));
                });
            } else {
                const empty = document.createElement("div");
                empty.className = "tree-item";
                empty.style.paddingLeft = "20px";
                empty.style.color = "var(--text-muted)";
                empty.innerText = "Empty Directory";
                childrenContainer.appendChild(empty);
            }
            wrapper.appendChild(item);
            wrapper.appendChild(childrenContainer);
        } else {
            item.addEventListener("click", (e) => {
                e.stopPropagation();
                fetchFile(node.path, node.name);
            });
            wrapper.appendChild(item);
        }
        return wrapper;
    }

    // Render Device Tree Node
    function renderDeviceNode(device) {
        const wrapper = document.createElement("div");
        wrapper.className = "tree-node";

        const item = document.createElement("div");
        item.className = "tree-item folder-node expanded";
        
        let icon = "🔌 ";
        if (device.type === "GPU") icon = "🖥️ ";
        else if (device.type === "Sensor") icon = "🌡️ ";
        else if (device.type === "Robot") icon = "🦀 ";

        item.innerText = icon + device.name;

        const childrenContainer = document.createElement("div");
        childrenContainer.className = "tree-children active";

        item.addEventListener("click", (e) => {
            e.stopPropagation();
            item.classList.toggle("expanded");
            childrenContainer.classList.toggle("active");
        });

        for (const [key, value] of Object.entries(device.metrics)) {
            const metric = document.createElement("div");
            metric.className = "device-metric";
            metric.innerHTML = `<span>${key}:</span><span class="val">${value}</span>`;
            childrenContainer.appendChild(metric);
        }

        wrapper.appendChild(item);
        wrapper.appendChild(childrenContainer);
        return wrapper;
    }

    // Fetch and display file content
    async function fetchFile(path, name) {
        activeProjectedFilePath = path;
        projectorFileName.innerText = `Projecting: ${path}`;
        codeContent.innerText = "Loading file content...";

        if (path.toLowerCase().includes("sdk_bricks") && path.toLowerCase().endsWith(".py")) {
            btnRunBrick.style.display = "block";
        } else {
            btnRunBrick.style.display = "none";
        }
        
        document.querySelector("[data-tab='projector']").click();

        try {
            const res = await fetch(`/api/file?path=${encodeURIComponent(path)}`);
            if (res.status === 200) {
                const text = await res.text();
                codeContent.innerText = text;
                addLogLine("info", `Projected source file: ${name}`);
            } else {
                codeContent.innerText = "Error: Failed to fetch file contents.";
            }
        } catch (err) {
            codeContent.innerText = `Error: ${err}`;
        }
    }

    // Fetch and populate trees on startup
    async function fetchTree() {
        try {
            const res = await fetch("/api/tree");
            const data = await res.json();

            fileTreeRoot.innerHTML = "";
            data.files.forEach(node => {
                fileTreeRoot.appendChild(renderFileNode(node));
            });

            deviceTreeRoot.innerHTML = "";
            data.devices.forEach(device => {
                deviceTreeRoot.appendChild(renderDeviceNode(device));
            });
        } catch (err) {
            console.error("Failed to build directory/device trees:", err);
        }
    }

    // Poll Telemetry Updates
    async function pollTelemetry() {
        try {
            const res = await fetch("/api/telemetry");
            const data = await res.json();

            headerCpu.innerText = data.cpu;
            headerRam.innerText = data.ram;
            headerGpuTemp.innerText = data.gpu.temp;

            // Feed real-time data to Projector histories
            const cpuVal = parseFloat(data.cpu) || 0;
            const gpuVal = parseFloat(data.gpu.util) || 0;
            cpuHistory.push(cpuVal);
            gpuHistory.push(gpuVal);
            if (cpuHistory.length > 30) cpuHistory.shift();
            if (gpuHistory.length > 30) gpuHistory.shift();

            // Redraw chart dynamically
            drawTelemetryChart();

            data.devices.forEach(device => {
                const existingNode = Array.from(deviceTreeRoot.children).find(child => 
                    child.querySelector(".tree-item").innerText.includes(device.name)
                );
                if (existingNode) {
                    const metricsContainer = existingNode.querySelector(".tree-children");
                    metricsContainer.innerHTML = "";
                    for (const [key, value] of Object.entries(device.metrics)) {
                        const metric = document.createElement("div");
                        metric.className = "device-metric";
                        metric.innerHTML = `<span>${key}:</span><span class="val">${value}</span>`;
                        metricsContainer.appendChild(metric);
                    }
                } else {
                    deviceTreeRoot.appendChild(renderDeviceNode(device));
                }
            });
        } catch (err) {
            console.error("Failed to poll telemetry metrics:", err);
        }
    }

    // Fetch DFMEA Table
    const dfmeaTableBody = document.getElementById("dfmea-table-body");
    async function fetchDFMEA() {
        try {
            const res = await fetch("/api/dfmea");
            const rules = await res.json();
            
            dfmeaTableBody.innerHTML = "";
            if (rules.length === 0) {
                dfmeaTableBody.innerHTML = "<tr><td colspan='11' style='text-align:center;'>No Rules Found in SQLite.</td></tr>";
                return;
            }

            rules.forEach(r => {
                const tr = document.createElement("tr");
                
                let severityClass = "severity-medium";
                if (r.severity >= 8) severityClass = "severity-high";

                const rpn = r.severity * (r.occurrence || 1) * (r.detection || 1);
                let rpnClass = "severity-medium";
                if (rpn > 100) {
                    rpnClass = "severity-high";
                }

                tr.innerHTML = `
                    <td>${r.id}</td>
                    <td>${escapeHTML(r.problem_point)}</td>
                    <td>${escapeHTML(r.failure_mode)}</td>
                    <td class="${severityClass}">${r.severity}</td>
                    <td>${r.occurrence || 1}</td>
                    <td>${r.detection || 1}</td>
                    <td class="${rpnClass}" style="font-weight: bold;">${rpn}</td>
                    <td>${escapeHTML(r.root_cause)}</td>
                    <td>${escapeHTML(r.prevention)}</td>
                    <td>${escapeHTML(r.corrective)}</td>
                    <td>
                        <button class="btn-action btn-edit" data-id="${r.id}">Edit</button>
                        <button class="btn-action btn-delete" data-id="${r.id}">Delete</button>
                    </td>
                `;
                
                // Add button listeners
                tr.querySelector(".btn-edit").addEventListener("click", () => editRule(r));
                tr.querySelector(".btn-delete").addEventListener("click", () => deleteRule(r.id));

                dfmeaTableBody.appendChild(tr);
            });
        } catch (err) {
            console.error("Failed to query DFMEA database:", err);
        }
    }

    // Edit rule modal popup
    function editRule(r) {
        ruleModalTitle.innerText = "Edit DFMEA Rule";
        ruleActionMode.value = "edit";
        ruleIdInput.value = r.id;
        ruleIdInput.disabled = true; // Primary key cannot be edited

        document.getElementById("rule-problem").value = r.problem_point;
        document.getElementById("rule-mode").value = r.failure_mode;
        document.getElementById("rule-severity").value = r.severity;
        document.getElementById("rule-occurrence").value = r.occurrence || 1;
        document.getElementById("rule-detection").value = r.detection || 1;
        document.getElementById("rule-cause").value = r.root_cause;
        document.getElementById("rule-prevention").value = r.prevention;
        document.getElementById("rule-corrective").value = r.corrective;

        ruleModal.classList.add("active");
    }

    // Delete rule request
    async function deleteRule(id) {
        if (!confirm(`Are you sure you want to delete DFMEA rule ${id}?`)) return;
        try {
            const res = await fetch(`/api/dfmea?id=${encodeURIComponent(id)}`, {
                method: "DELETE"
            });
            const result = await res.json();
            if (result.status === "success") {
                addLogLine("success", `[DFMEA] Deleted rule: ${id}`);
                fetchDFMEA();
            }
        } catch (err) {
            alert("Delete failed: " + err);
        }
    }

    // Poll logs dynamically and append
    let displayedLogs = new Set();
    async function pollLogs() {
        try {
            const res = await fetch("/api/logs");
            const logs = await res.json();
            
            logs.forEach(line => {
                if (!displayedLogs.has(line)) {
                    displayedLogs.add(line);
                    
                    const time = new Date().toLocaleTimeString();
                    const div = document.createElement("div");
                    
                    let type = "info";
                    if (line.toLowerCase().includes("fail") || line.toLowerCase().includes("error") || line.toLowerCase().includes("fatal") || line.toLowerCase().includes("critical")) {
                        type = "error";
                    } else if (line.toLowerCase().includes("ok") || line.toLowerCase().includes("success") || line.toLowerCase().includes("pass")) {
                        type = "success";
                    }
                    
                    div.className = `log-line ${type}`;
                    div.innerText = line;
                    consoleLogs.appendChild(div);
                }
            });
            
            // Scroll to bottom if new lines are added
            if (logs.length > 0) {
                consoleLogs.scrollTop = consoleLogs.scrollHeight;
            }
        } catch (err) {
            console.error("Failed to poll log stream:", err);
        }
    }

    // Send chat message
    async function sendMessage() {
        const prompt = chatInput.value.trim();
        if (!prompt) return;

        appendBubble("sent", prompt);
        chatInput.value = "";

        const typingId = "typing_" + Date.now();
        const typingBubble = document.createElement("div");
        typingBubble.className = "message-bubble received typing";
        typingBubble.id = typingId;
        typingBubble.innerHTML = `<p><i>Gemini is writing...</i></p>`;
        chatMessages.appendChild(typingBubble);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        try {
            const res = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: prompt })
            });
            const data = await res.json();
            
            const typingNode = document.getElementById(typingId);
            if (typingNode) typingNode.remove();
            
            // Render offline indicator badge if prefix matches
            if (data.response.includes("[OFFLINE DEFENSE ACTIVATED]")) {
                tgAgentName.innerText = "Local AI Controller";
                tgAgentStatus.innerText = "offline mode";
                tgAgentStatus.className = "tg-status-offline";
            } else {
                tgAgentName.innerText = "Gemini AI Agent";
                tgAgentStatus.innerText = "online";
                tgAgentStatus.className = "tg-status-online";
            }

            appendBubble("received", data.response);
            addLogLine("info", `Gemini returned AI diagnostic response.`);
        } catch (err) {
            const typingNode = document.getElementById(typingId);
            if (typingNode) typingNode.remove();
            appendBubble("received", `Error connecting to AI backend: ${err}`);
        }
    }

    function appendBubble(sender, text) {
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const bubble = document.createElement("div");
        bubble.className = `message-bubble ${sender}`;
        bubble.innerHTML = `<p>${escapeHTML(text)}</p><span class="time">${time}</span>`;
        chatMessages.appendChild(bubble);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function escapeHTML(str) {
        if (str === null || str === undefined) return "";
        return String(str).replace(/[&<>'"]/g, 
            tag => ({
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                "'": '&#39;',
                '"': '&quot;'
            }[tag] || tag)
        );
    }

    btnSend.addEventListener("click", sendMessage);
    chatInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") sendMessage();
    });

    async function triggerChatCommand(messageText) {
        appendBubble("user", messageText);
        
        const typingBubble = document.createElement("div");
        typingBubble.className = "message-bubble system typing";
        typingBubble.innerText = "Chiling is thinking...";
        chatMessages.appendChild(typingBubble);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        try {
            const res = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: messageText })
            });
            const result = await res.json();
            
            chatMessages.removeChild(typingBubble);
            
            if (result.response) {
                appendBubble("system", result.response);
            } else {
                appendBubble("system", "Error executing command.");
            }
        } catch (err) {
            if (chatMessages.contains(typingBubble)) {
                chatMessages.removeChild(typingBubble);
            }
            appendBubble("system", "Failed to connect to system agent.");
        }
    }

    const btnProcDoctor = document.getElementById("btn-proc-doctor");
    const btnProcRobot = document.getElementById("btn-proc-robot");
    const btnProcSensor = document.getElementById("btn-proc-sensor");
    const btnProcSync = document.getElementById("btn-proc-sync");
    
    if (btnProcDoctor) {
        btnProcDoctor.addEventListener("click", () => triggerChatCommand("/doctor"));
    }
    if (btnProcRobot) {
        btnProcRobot.addEventListener("click", () => triggerChatCommand("/run_brick Robot_Movement.py"));
    }
    if (btnProcSensor) {
        btnProcSensor.addEventListener("click", () => triggerChatCommand("/run_brick Sensor_Sampling.py"));
    }
    if (btnProcSync) {
        btnProcSync.addEventListener("click", () => triggerChatCommand("/sync"));
    }

    btnRunBrick.addEventListener("click", async () => {
        if (!activeProjectedFilePath) return;

        btnRunBrick.disabled = true;
        btnRunBrick.innerText = "Running...";
        addLogLine("info", `Dispatching brick run command for: ${activeProjectedFilePath}`);

        try {
            const res = await fetch("/api/run-brick", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ path: activeProjectedFilePath })
            });
            const data = await res.json();
            
            if (data.status === "success") {
                addLogLine("success", `[System] Brick finished execution with exit code: ${data.exit_code}`);
                document.querySelector("[data-tab='console']").click();
            } else {
                addLogLine("error", `[System] Brick failed to run: ${data.message}`);
            }
        } catch (err) {
            addLogLine("error", `[System] Failed to connect to runner endpoint: ${err}`);
        } finally {
            btnRunBrick.disabled = false;
            btnRunBrick.innerText = "🚀 Run Brick";
        }
    });

    // Fetch Cloud Sync & Sandbox Status
    // Fetch Cloud Sync & Sandbox Status
    const headerCloudSync = document.getElementById("header-cloud-sync");
    const cloudLastSync = document.getElementById("cloud-last-sync");
    const cloudTakeoverState = document.getElementById("cloud-takeover-state");
    const blockedScriptsTableBody = document.getElementById("blocked-scripts-table-body");
    const approvalsTableBody = document.getElementById("approvals-table-body");
    const cloudTgStatus = document.getElementById("cloud-tg-status");
    const cloudTgChatId = document.getElementById("cloud-tg-chat-id");
    const gooseLogContainer = document.getElementById("goose-log-container");
    const btnLangToggle = document.getElementById("btn-lang-toggle");
    
    // Flow Visualizer Elements
    const taskFlowViz = document.getElementById("task-flow-viz");
    const flowStepsContainer = document.getElementById("flow-steps-container");
    let activeFlowTaskId = null;

    // Translations Dictionary
    const translations = {
        "zh": {
            "header-title": "GENESIS 智慧協同控制中心",
            "tab-projector": "🎬 代碼投影中心",
            "tab-dfmea": "📋 DFMEA 矩陣",
            "tab-console": "📟 控制台日誌",
            "tab-cloud": "☁️ 雲端指揮部",
            "btn-add-device": "＋ 新增設備",
            "title-devices": "🖥️ 設備與感測器",
            "title-workspace": "📁 專案代碼庫",
            "title-procedures": "⚡ 快速預存指令",
            "cloud-sync-title": "☁️ 雲地同步與接管狀態",
            "last-sync-label": "最後雲地同步時間",
            "takeover-label": "雲端自主接管狀態",
            "mirror-label": "鏡像備份生成狀態",
            "sandbox-title": "🛡️ AST 沙盒熔斷阻斷紀錄",
            "hitl-title": "🛡️ 主管決策簽核中心 (HITL 隊列)",
            "tg-title": "🤖 Telegram 遠端通訊狀態",
            "goose-title": "🦢 Goose AI 執行與監控防禦日誌 (Stage 3 & 4)",
            "th-task-id": "任務 ID",
            "th-script": "積木腳本",
            "th-time": "時間",
            "th-status": "狀態",
            "th-action": "操作 / 動作",
            "th-decision": "主管審查決策",
            "placeholder-chat": "輸入訊息給 Gemini (即時處理與主管意見交流)...",
            "tg-agent-name": "🧠 Gemini AI 即時處理與主管意見交流",
            "btn-send": "發送",
            "status-connected": "已連接",
            "status-disconnected": "已離線",
            "status-active": "接管中",
            "status-inactive": "待命靜止",
            "status-generated": "已生成",
            "status-missing": "未生成",
            "status-healthy": "健康",
            "status-meltdown": "安全熔斷",
            "lang-toggle": "🌐 繁中 / EN",
            "btn-proc-doctor": "🩺 系統一鍵健檢 (Doctor)",
            "btn-proc-robot": "🦀 機械手臂軌跡 (Robot)",
            "btn-proc-sensor": "🌡️ 數據採樣監控 (Sensor)",
            "btn-proc-sync": "☁️ 雲地心跳對齊 (Sync)",
            "flow-title": "🚀 任務編譯與生命週期追蹤",
            "tab-home": "🏠 綜合指揮中心",
            "home-sec-status": "🖥️ 系統軟硬體實時監控",
            "home-sec-dev": "🚀 今日研發進度與完成項目",
            "home-sec-doctor": "🩺 Doctor 自癒派遣中心",
            "alarm-title": "系統異常告警：主動派遣 Doctor 自癒修復中...",
            "badge-repair": "修補中",
            "progress-label": "研發進度達成率",
            "home-title-pending": "進行中 / 待審任務",
            "home-title-completed": "今日已完成項目",
            "tab-clawlibrary": "🏢 2D 虛擬辦公室",
            "tab-nodered": "🔴 Node-RED 儀表板"
        },
        "en": {
            "header-title": "GENESIS CONTROL STATION",
            "tab-projector": "🎬 Code Projector",
            "tab-dfmea": "📋 DFMEA Matrix",
            "tab-console": "📟 Console Logs",
            "tab-cloud": "☁️ Cloud Command",
            "btn-add-device": "＋ Add Device",
            "title-devices": "🖥️ DEVICES & SENSORS",
            "title-workspace": "📁 WORKSPACE FILES",
            "title-procedures": "⚡ STORED PROCEDURES",
            "cloud-sync-title": "☁️ Cloud Synchronization & Takeover Status",
            "last-sync-label": "Last Cloud Sync",
            "takeover-label": "Cloud Takeover State",
            "mirror-label": "HTML/CSV Mirrors",
            "sandbox-title": "🛡️ AST Sandbox Blocked Drafts",
            "hitl-title": "🛡️ Supervisor Decision Center (HITL Queue)",
            "tg-title": "🤖 Telegram Remote Integration",
            "goose-title": "🦢 Goose AI Execution & DFMEA Defense (Stage 3 & 4)",
            "th-task-id": "Task ID",
            "th-script": "Script Name",
            "th-time": "Timestamp",
            "th-status": "Status",
            "th-action": "Action",
            "th-decision": "Decision Action",
            "placeholder-chat": "Type a message to Gemini (Instant processing & discussion)...",
            "tg-agent-name": "🧠 Gemini AI Instant Processor & Communication",
            "btn-send": "Send",
            "status-connected": "CONNECTED",
            "status-disconnected": "OFFLINE",
            "status-active": "Active",
            "status-inactive": "Inactive",
            "status-generated": "Generated",
            "status-missing": "Missing",
            "status-healthy": "HEALTHY",
            "status-meltdown": "MELTDOWN",
            "lang-toggle": "🌐 EN / 繁中",
            "btn-proc-doctor": "🩺 Diagnostic (Doctor)",
            "btn-proc-robot": "🦀 Robot Path (Robot)",
            "btn-proc-sensor": "🌡️ Sensor Sampling (Sensor)",
            "btn-proc-sync": "☁️ Cloud Sync (Sync)",
            "flow-title": "🚀 Task Lifecycle Flow",
            "tab-home": "🏠 Home Control Center",
            "home-sec-status": "🖥️ Live System Hardware & Software Monitor",
            "home-sec-dev": "🚀 R&D Progress & Accomplishments",
            "home-sec-doctor": "🩺 Doctor Autonomous Healing Dispatch",
            "alarm-title": "System Abnormality: Doctor Dispatched for Healing...",
            "badge-repair": "REPAIR ACTIVE",
            "progress-label": "R&D Completion Progress",
            "home-title-pending": "In-Progress / Awaiting Tasks",
            "home-title-completed": "Today's Completed Items",
            "tab-clawlibrary": "🏢 2D Virtual Office",
            "tab-nodered": "🔴 Node-RED Dashboard"
        }
    };

    let currentLang = localStorage.getItem("lang") || "zh";

    function applyLanguage(lang) {
        currentLang = lang;
        localStorage.setItem("lang", lang);
        
        document.querySelectorAll("[data-i18n]").forEach(el => {
            const key = el.getAttribute("data-i18n");
            if (translations[lang] && translations[lang][key]) {
                if (el.tagName === "INPUT") {
                    el.placeholder = translations[lang][key];
                } else {
                    el.innerText = translations[lang][key];
                }
            }
        });
        document.title = lang === "zh" ? "Genesis 智慧協同控制中心" : "Genesis Control Station";
    }

    if (btnLangToggle) {
        btnLangToggle.addEventListener("click", () => {
            const nextLang = currentLang === "zh" ? "en" : "zh";
            applyLanguage(nextLang);
            // Re-render flow visualizer to apply language if it's active
            if (activeFlowTaskId) {
                pollCloudStatus();
            }
        });
    }

    function renderTaskFlow(task) {
        if (!taskFlowViz || !flowStepsContainer) return;
        
        taskFlowViz.style.display = "block";
        
        const steps = [
            { id: "S1", zh: "大腦設計 [S1]", en: "Design [S1]", icon: "🧠" },
            { id: "S2", zh: "安全沙盒 [S2]", en: "Sandbox [S2]", icon: "🛡️" },
            { id: "S3", zh: "主管審批", en: "Approval", icon: "🔑" },
            { id: "S4", zh: "地端編譯 [S3]", en: "Goose S3", icon: "🦢" },
            { id: "S5", zh: "防禦監控 [S4]", en: "Monitor S4", icon: "📡" }
        ];
        
        let states = { S1: "success", S2: "success", S3: "pending", S4: "pending", S5: "pending" };
        const status = task.status;
        
        if (status === "BLOCKED_BY_SANDBOX") {
            states.S2 = "error";
        } else if (status === "AWAITING_APPROVAL") {
            states.S3 = "active-yellow";
        } else if (status === "PENDING") {
            states.S3 = "success";
            states.S4 = "active-blue";
        } else if (status === "COMPLETED") {
            states.S3 = "success";
            states.S4 = "success";
            states.S5 = "success";
        } else if (status === "REJECTED") {
            states.S3 = "error";
        }
        
        flowStepsContainer.innerHTML = "";
        
        steps.forEach((step) => {
            const stepDiv = document.createElement("div");
            stepDiv.className = `flow-step state-${states[step.id].split("-")[0]}`;
            
            const nodeDiv = document.createElement("div");
            nodeDiv.className = `step-node state-${states[step.id]}`;
            nodeDiv.title = currentLang === "zh" ? step.zh : step.en;
            nodeDiv.innerText = step.icon;
            
            const labelDiv = document.createElement("div");
            labelDiv.className = "step-label";
            labelDiv.innerText = currentLang === "zh" ? step.zh : step.en;
            
            stepDiv.appendChild(nodeDiv);
            stepDiv.appendChild(labelDiv);
            flowStepsContainer.appendChild(stepDiv);
        });
        
        const numConnectors = steps.length - 1;
        setTimeout(() => {
            const flowWidth = flowStepsContainer.clientWidth;
            const nodeWidth = 38;
            const usableWidth = flowWidth - (nodeWidth * steps.length);
            const stepDistance = usableWidth / numConnectors + nodeWidth;
            
            for (let i = 0; i < numConnectors; i++) {
                const connector = document.createElement("div");
                connector.className = "step-connector";
                
                const leftState = states[steps[i].id];
                const rightState = states[steps[i+1].id];
                
                let connectorState = "pending";
                if (leftState === "success" && rightState === "success") {
                    connectorState = "success";
                } else if (leftState === "success" && rightState.startsWith("active")) {
                    connectorState = "active";
                }
                
                connector.className += ` state-${connectorState}`;
                
                const leftPos = (i * stepDistance) + (nodeWidth / 2) + (nodeWidth / 2);
                const width = stepDistance - nodeWidth;
                
                connector.style.left = `${leftPos}px`;
                connector.style.width = `${width}px`;
                
                flowStepsContainer.appendChild(connector);
            }
        }, 50);
    }

    async function approveTask(taskId) {
        if (!confirm(`Are you sure you want to APPROVE task ${taskId}?`)) return;
        try {
            const res = await fetch("/api/approve-task", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ task_id: taskId })
            });
            const result = await res.json();
            if (result.status === "success") {
                addLogLine("success", `[HITL] Approved task ${taskId}. Transitioned to: ${result.next_status}`);
                pollCloudStatus();
            }
        } catch (err) {
            alert("Approve failed: " + err);
        }
    }

    async function rejectTask(taskId) {
        if (!confirm(`Are you sure you want to REJECT and archive task ${taskId}?`)) return;
        try {
            const res = await fetch("/api/reject-task", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ task_id: taskId })
            });
            const result = await res.json();
            if (result.status === "success") {
                addLogLine("error", `[HITL] Rejected and archived task ${taskId}.`);
                pollCloudStatus();
            }
        } catch (err) {
            alert("Reject failed: " + err);
        }
    }

    // Telemetry Projector Variables & Engine
    let cpuHistory = [];
    let gpuHistory = [];
    let chartMode = "allocation"; // default
    let autoCycleInterval = null;

    function startAutoCycle() {
        if (autoCycleInterval) clearInterval(autoCycleInterval);
        autoCycleInterval = setInterval(() => {
            if (chartMode === "allocation") {
                setChartMode("trends", false);
            } else if (chartMode === "trends") {
                setChartMode("compare", false);
            } else {
                setChartMode("allocation", false);
            }
        }, 5000); // Cycle every 5 seconds
    }

function setChartMode(mode, isManual = false) {
    chartMode = mode;
    document.querySelectorAll(".btn-proj").forEach(b => b.classList.remove("active"));
    if (mode === "allocation") document.getElementById("btn-chart-alloc").classList.add("active");
    if (mode === "trends") document.getElementById("btn-chart-trends").classList.add("active");
    if (mode === "compare") document.getElementById("btn-chart-compare").classList.add("active");
    if (mode === "media") document.getElementById("btn-proj-media").classList.add("active");
    if (mode === "ai-intelligence") document.getElementById("btn-proj-ai").classList.add("active");

    const canvas = document.getElementById("telemetry-chart-canvas");
    const overlay = document.getElementById("projector-overlay-content");

    if (mode === "media" || mode === "ai-intelligence") {
        if (canvas) canvas.style.display = "none";
        if (overlay) {
            overlay.style.display = "block";
            if (mode === "media") {
                renderProjectorMediaPanel();
            } else {
                renderProjectorAIPanel();
            }
        }
        if (autoCycleInterval && isManual) clearInterval(autoCycleInterval);
    } else {
        if (overlay) overlay.style.display = "none";
        if (canvas) canvas.style.display = "block";
        drawTelemetryChart();
        if (isManual) {
            startAutoCycle();
        }
    }
}

const btnChartAlloc = document.getElementById("btn-chart-alloc");
const btnChartTrends = document.getElementById("btn-chart-trends");
const btnChartCompare = document.getElementById("btn-chart-compare");
const btnProjMedia = document.getElementById("btn-proj-media");
const btnProjAI = document.getElementById("btn-proj-ai");

if (btnChartAlloc) btnChartAlloc.addEventListener("click", () => setChartMode("allocation", true));
if (btnChartTrends) btnChartTrends.addEventListener("click", () => setChartMode("trends", true));
if (btnChartCompare) btnChartCompare.addEventListener("click", () => setChartMode("compare", true));
if (btnProjMedia) btnProjMedia.addEventListener("click", () => setChartMode("media", true));
if (btnProjAI) btnProjAI.addEventListener("click", () => setChartMode("ai-intelligence", true));

    // Holographic Telemetry Projector Media Functions
    async function projectImage(filePath) {
        const preview = document.getElementById("proj-image-preview-container");
        if (!preview) return;
        
        preview.innerHTML = `<span style="color: #fbbf24; font-size:11px;">Projecting image...</span>`;
        try {
            const res = await fetch("/api/project-media", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ action: "project", path: filePath })
            });
            const data = await res.json();
            if (data.status === "success") {
                preview.innerHTML = `
                    <img src="/api/image-loader?path=${encodeURIComponent(filePath)}" style="max-width: 100%; max-height: 100%; object-fit: contain; box-shadow: 0 0 15px rgba(96, 165, 250, 0.4); border: 1px solid #60a5fa;">
                    <div style="position: absolute; bottom: 8px; left: 8px; background: rgba(0,0,0,0.7); padding: 2px 6px; border-radius: 4px; font-size: 10px; color: #60a5fa;">Projected Asset: ${data.filename}</div>
                `;
                addLogLine("success", `Holographic image projected successfully: ${data.filename}`);
                loadProjectorSavedProjections();
            } else {
                preview.innerHTML = `<span style="color: #ef4444; font-size:11px;">Error: ${data.message}</span>`;
            }
        } catch (err) {
            preview.innerHTML = `<span style="color: #ef4444; font-size:11px;">Connection error: ${err.message}</span>`;
        }
    }

    async function loadProjectorTimeline() {
        const container = document.getElementById("proj-timeline-container");
        if (!container) return;
        
        container.innerHTML = "Querying history database...";
        try {
            const res = await fetch("/api/project-media?action=timeline");
            const data = await res.json();
            container.innerHTML = "";
            if (data.length === 0) {
                container.innerHTML = "No historical progress records found in database.";
                return;
            }
            data.forEach(item => {
                const div = document.createElement("div");
                div.style.borderBottom = "1px solid rgba(255,255,255,0.05)";
                div.style.paddingBottom = "4px";
                div.innerHTML = `<span style="color: #fbbf24;">[${item.timestamp}]</span> <strong>${item.actor}</strong>: ${escapeHTML(item.content)}`;
                container.appendChild(div);
            });
        } catch (err) {
            container.innerHTML = `Error: ${err.message}`;
        }
    }

    async function loadProjectorSavedProjections() {
        const container = document.getElementById("proj-db-container");
        if (!container) return;
        
        container.innerHTML = "Fetching saved list...";
        try {
            const res = await fetch("/api/project-media?action=list");
            const data = await res.json();
            container.innerHTML = "";
            if (data.length === 0) {
                container.innerHTML = "No projections stored in database.";
                return;
            }
            data.forEach(item => {
                const div = document.createElement("div");
                div.style.display = "flex";
                div.style.justifyContent = "space-between";
                div.style.alignItems = "center";
                div.innerHTML = `
                    <span style="color: #a5b4fc; cursor: pointer; text-decoration: underline; max-width:70%; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;" onclick="window.projectSavedItem('${escapeHTML(item.path)}')">${escapeHTML(item.filename)}</span>
                    <span style="color: #6b7280; font-size: 10px;">${item.timestamp}</span>
                `;
                container.appendChild(div);
            });
        } catch (err) {
            container.innerHTML = `Error: ${err.message}`;
        }
    }
    window.projectSavedItem = (path) => {
        const input = document.getElementById("proj-img-input");
        if (input) input.value = path;
        projectImage(path);
    };

    async function renderProjectorMediaPanel() {
        const overlay = document.getElementById("projector-overlay-content");
        if (!overlay) return;
        
        overlay.innerHTML = `
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; height: 100%; font-size: 13px;">
                <!-- Left panel: Projection Controls -->
                <div style="background: rgba(255,255,255,0.02); padding: 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); display: flex; flex-direction: column; gap: 10px;">
                    <h4 style="margin: 0; color: #60a5fa;">📷 Holographic Image / Photo Projector</h4>
                    <div style="display: flex; gap: 8px;">
                        <input type="text" id="proj-img-input" placeholder="e.g. C:/Genesis/logo.png or URL" style="flex:1; background: #000; border: 1px solid #555; color: #fff; padding: 4px 8px; border-radius: 4px; font-family: monospace; font-size: 11px;">
                        <button class="btn-submit" id="btn-project-img-submit" style="width: auto; padding: 4px 10px; margin:0; background: #3b82f6; font-size:11px; font-weight:bold;">Project</button>
                    </div>
                    <div id="proj-image-preview-container" style="flex: 1; border: 1px dashed rgba(255,255,255,0.15); border-radius: 6px; display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden; background: #050510;">
                        <span style="color: #6b7280; font-size: 11px;">No photo projected yet.</span>
                    </div>
                </div>
                
                <!-- Right panel: Timeline & Projections DB -->
                <div style="display: flex; flex-direction: column; gap: 10px; justify-content: space-between;">
                    <div style="background: rgba(255,255,255,0.02); padding: 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); flex: 1.2; display: flex; flex-direction: column; gap: 8px;">
                        <h4 style="margin: 0; color: #10b981; display: flex; justify-content: space-between; align-items: center;">
                            <span>📜 History Timeline Progress</span>
                            <button class="btn-submit" id="btn-load-timeline" style="background: none; border: 1px solid #10b981; color: #10b981; cursor: pointer; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; width: auto; margin:0; line-height:1;">Reload</button>
                        </h4>
                        <div id="proj-timeline-container" style="flex: 1; overflow-y: auto; max-height: 110px; display: flex; flex-direction: column; gap: 6px; font-size: 11px; color: #a7f3d0; background: #05100a; padding: 6px; border-radius: 4px; border: 1px solid rgba(16, 185, 129, 0.15);">
                            Loading history timeline...
                        </div>
                    </div>
                    
                    <div style="background: rgba(255,255,255,0.02); padding: 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); flex: 0.8; display: flex; flex-direction: column; gap: 8px;">
                        <h4 style="margin: 0; color: #fbbf24;">📂 Saved Projections Database</h4>
                        <div id="proj-db-container" style="flex: 1; overflow-y: auto; max-height: 60px; font-size: 11px; background: #100a05; padding: 6px; border-radius: 4px; border: 1px solid rgba(251, 191, 36, 0.15); display: flex; flex-direction: column; gap: 4px;">
                            No projections saved.
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Bind media events
        document.getElementById("btn-project-img-submit").addEventListener("click", () => {
            const path = document.getElementById("proj-img-input").value.trim();
            if (path) projectImage(path);
        });
        document.getElementById("btn-load-timeline").addEventListener("click", loadProjectorTimeline);
        
        loadProjectorTimeline();
        loadProjectorSavedProjections();
    }

    function drawTelemetryChart() {
        const canvas = document.getElementById("telemetry-chart-canvas");
        if (!canvas) return;
        const ctx = canvas.getContext("2d");
        const w = canvas.width;
        const h = canvas.height;
        ctx.clearRect(0, 0, w, h);
        
        const insightEl = document.getElementById("proj-insight");
        
        // Ensure some initial history data is populated
        if (cpuHistory.length === 0) {
            for (let i = 0; i < 15; i++) {
                cpuHistory.push(15 + Math.sin(i * 0.5) * 5 + Math.random() * 3);
                gpuHistory.push(35 + Math.cos(i * 0.5) * 8 + Math.random() * 4);
            }
        }
        
        if (chartMode === "allocation") {
            // Draw Donut charts side-by-side with enlarged metrics
            const donuts = [
                { x: w * 0.28, y: h * 0.5, r: 75, title: currentLang === "zh" ? "NAS 空間分配 (NAS Storage)" : "NAS Storage Alloc", used: 4.2, total: 16.0, unit: "TB", color: "#3b82f6" },
                { x: w * 0.72, y: h * 0.5, r: 75, title: currentLang === "zh" ? "RTX VRAM 佔用 (RTX VRAM)" : "RTX VRAM Allocation", used: 5.4, total: 12.0, unit: "GB", color: "#10b981" }
            ];
            
            donuts.forEach(d => {
                const pct = d.used / d.total;
                
                // Draw background arc
                ctx.beginPath();
                ctx.arc(d.x, d.y, d.r, 0, 2 * Math.PI);
                ctx.lineWidth = 16;
                ctx.strokeStyle = "#222";
                ctx.stroke();
                
                // Draw active progress arc
                ctx.beginPath();
                ctx.arc(d.x, d.y, d.r, -Math.PI / 2, (-Math.PI / 2) + (2 * Math.PI * pct));
                ctx.lineWidth = 16;
                ctx.strokeStyle = d.color;
                ctx.shadowColor = d.color;
                ctx.shadowBlur = 12;
                ctx.stroke();
                ctx.shadowBlur = 0; // reset
                
                // Text details (Enlarged)
                ctx.font = "bold 24px Outfit, sans-serif";
                ctx.fillStyle = "#ffffff";
                ctx.textAlign = "center";
                ctx.textBaseline = "middle";
                ctx.fillText(`${Math.round(pct * 100)}%`, d.x, d.y - 10);
                
                ctx.font = "13px JetBrains Mono, monospace";
                ctx.fillStyle = "#9ca3af";
                ctx.fillText(`${d.used}/${d.total} ${d.unit}`, d.x, d.y + 18);
                
                // Label title above donut (Enlarged)
                ctx.font = "bold 16px Outfit, sans-serif";
                ctx.fillStyle = "#a5b4fc";
                ctx.fillText(d.title, d.x, d.y - d.r - 24);
            });
            
            if (insightEl) {
                insightEl.innerText = currentLang === "zh" ? 
                    "NAS 及顯卡虛擬記憶體分配皆處於綠色安全界限，系統冗餘率大於 55%。" : 
                    "NAS and VRAM structures are within normal boundaries. System headroom exceeds 55%.";
            }
        } 
        else if (chartMode === "trends") {
            // Draw Line Chart showing load trends with enlarged typography
            const padding = 45;
            const graphW = w - padding * 2;
            const graphH = h - padding * 2;
            
            // Draw axis lines
            ctx.beginPath();
            ctx.moveTo(padding, padding);
            ctx.lineTo(padding, h - padding);
            ctx.lineTo(w - padding, h - padding);
            ctx.strokeStyle = "#374151";
            ctx.lineWidth = 2;
            ctx.stroke();
            
            // Axis labels (Enlarged)
            ctx.font = "12px JetBrains Mono, monospace";
            ctx.fillStyle = "#9ca3af";
            ctx.textAlign = "right";
            ctx.textBaseline = "middle";
            ctx.fillText("100%", padding - 8, padding);
            ctx.fillText("50%", padding - 8, padding + graphH / 2);
            ctx.fillText("0%", padding - 8, h - padding);
            
            ctx.textAlign = "center";
            ctx.font = "bold 14px Outfit, sans-serif";
            ctx.fillText(currentLang === "zh" ? "時間推移曲線圖 (最近 30 次監測次數)" : "Live Timeline (last 30 ticks)", w / 2, h - 14);
            
            // Legend (Enlarged)
            ctx.font = "bold 13px Outfit, sans-serif";
            ctx.fillStyle = "#10b981";
            ctx.fillText("● CPU Load", w * 0.4, padding - 15);
            ctx.fillStyle = "#3b82f6";
            ctx.fillText("● GPU Load", w * 0.6, padding - 15);
            
            const drawLine = (history, color) => {
                if (history.length < 2) return;
                ctx.beginPath();
                const step = graphW / (history.length - 1);
                
                for (let i = 0; i < history.length; i++) {
                    const x = padding + (i * step);
                    const val = history[i];
                    const y = (h - padding) - (val / 100) * graphH;
                    if (i === 0) ctx.moveTo(x, y);
                    else ctx.lineTo(x, y);
                }
                
                ctx.lineWidth = 4;
                ctx.strokeStyle = color;
                ctx.shadowColor = color;
                ctx.shadowBlur = 10;
                ctx.stroke();
                ctx.shadowBlur = 0; // reset
            };
            
            drawLine(cpuHistory, "#10b981");
            drawLine(gpuHistory, "#3b82f6");
            
            if (insightEl) {
                insightEl.innerText = currentLang === "zh" ? 
                    "歷史負載推移圖表明：當前無顯著編譯阻塞，地端運算資源健康狀況為優。" : 
                    "Historical load trends show no calculation bottlenecks. Local computational state is excellent.";
            }
        } 
        else if (chartMode === "compare") {
            // Draw comparison side-by-side bars with enlarged metrics
            const metrics = [
                { name: "CPU Load", today: Math.round(cpuHistory.reduce((a, b) => a + b, 0) / cpuHistory.length) || 22, yesterday: 28 },
                { name: "GPU Load", today: Math.round(gpuHistory.reduce((a, b) => a + b, 0) / gpuHistory.length) || 42, yesterday: 48 },
                { name: "RAM Load", today: 49, yesterday: 52 }
            ];
            
            const barW = 35;
            const gap = 160;
            const startX = w / 2 - gap;
            
            metrics.forEach((m, idx) => {
                const cx = startX + idx * gap;
                const baseY = h - 45;
                const scale = 1.8;
                
                // Yesterday Bar (Gray)
                const yHeight = m.yesterday * scale;
                ctx.fillStyle = "#374151";
                ctx.fillRect(cx - barW - 4, baseY - yHeight, barW, yHeight);
                
                // Today Bar (Gradient)
                const tHeight = m.today * scale;
                const grad = ctx.createLinearGradient(0, baseY - tHeight, 0, baseY);
                grad.addColorStop(0, "#60a5fa");
                grad.addColorStop(1, "#3b82f6");
                ctx.fillStyle = grad;
                ctx.fillRect(cx + 4, baseY - tHeight, barW, tHeight);
                
                // Value text labels above bars (Enlarged)
                ctx.font = "12px JetBrains Mono, monospace";
                ctx.textAlign = "center";
                ctx.fillStyle = "#9ca3af";
                ctx.fillText(`${m.yesterday}%`, cx - barW/2 - 4, baseY - yHeight - 8);
                ctx.fillStyle = "#60a5fa";
                ctx.fillText(`${m.today}%`, cx + barW/2 + 4, baseY - tHeight - 8);
                
                // Metric label below bars (Enlarged)
                ctx.font = "bold 14px Outfit, sans-serif";
                ctx.fillStyle = "#e5e7eb";
                ctx.fillText(m.name, cx, baseY + 20);
            });
            
            // Legend (Enlarged)
            ctx.font = "bold 13px Outfit, sans-serif";
            ctx.fillStyle = "#60a5fa";
            ctx.fillText(currentLang === "zh" ? "■ Today (今日平均)" : "■ Today (Avg)", w * 0.38, 28);
            ctx.fillStyle = "#374151";
            ctx.fillText(currentLang === "zh" ? "■ Yesterday (昨日基準)" : "■ Yesterday (Baseline)", w * 0.62, 28);
            
            if (insightEl) {
                insightEl.innerText = currentLang === "zh" ? 
                    "相較於昨日基準，今日整體 CPU 負載因優化沙盒 AST 解析而降低了 15%。" : 
                    "Compared to yesterday's baseline, CPU load today has decreased by 15% due to optimized AST resolution.";
            }
        }
    }

    window.latestAIIntelligenceData = null;
async function fetchAIIntelligence() {
    try {
        const res = await fetch("/api/ai-intelligence");
        if (res.status === 200) {
            window.latestAIIntelligenceData = await res.json();
            if (typeof chartMode !== 'undefined' && chartMode === "ai-intelligence") {
                renderProjectorAIPanel();
            }
        }
    } catch (err) {
        console.error("Failed to fetch AI intelligence data:", err);
    }
}

    async function pollCloudStatus() {
        try {
            const res = await fetch("/api/cloud-status");
            if (res.status !== 200) return;
            const data = await res.json();

            // 1. Update Header Badge
            if (data.last_sync_time === "N/A") {
                headerCloudSync.innerText = currentLang === "zh" ? "已離線" : "OFFLINE";
                headerCloudSync.style.color = "#ef4444";
            } else if (data.is_cloud_active) {
                headerCloudSync.innerText = currentLang === "zh" ? "接管中" : "CLOUDACTIVE";
                headerCloudSync.style.color = "#f59e0b";
            } else {
                headerCloudSync.innerText = currentLang === "zh" ? "已連接" : "ONLINE";
                headerCloudSync.style.color = "#10b981";
            }

            // 2. Update Tab Cards
            cloudLastSync.innerText = data.last_sync_time;
            cloudTakeoverState.innerText = data.is_cloud_active ? 
                (currentLang === "zh" ? "雲端接管 (啟動中)" : "Cloud Takeover (Active)") : 
                (currentLang === "zh" ? "待命靜止 (本地控制)" : "Inactive (Local Control)");
            cloudTakeoverState.style.color = data.is_cloud_active ? "#f59e0b" : "#9ca3af";

            // 3. Update Telegram Remote Integration Status
            if (cloudTgStatus) {
                cloudTgStatus.innerText = data.tg_active ? 
                    (currentLang === "zh" ? "已連線" : "Online") : 
                    (currentLang === "zh" ? "未啟動" : "Offline");
                cloudTgStatus.style.color = data.tg_active ? "#10b981" : "#ef4444";
            }
            if (cloudTgChatId) {
                cloudTgChatId.innerText = data.tg_chat_id || "N/A";
                cloudTgChatId.style.color = data.tg_chat_id ? "#10b981" : "#9ca3af";
            }

            // 4. Update Goose AI Executor Telemetry
            if (gooseLogContainer) {
                gooseLogContainer.innerHTML = "";
                if (!data.goose_logs || data.goose_logs.length === 0) {
                    gooseLogContainer.innerHTML = `<div style="color: #888;">${currentLang === "zh" ? "尚無執行日誌，系統安全無虞。" : "No execution logs found. System secure."}</div>`;
                } else {
                    data.goose_logs.forEach(l => {
                        const div = document.createElement("div");
                        div.className = "log-line";
                        if (l.includes("[ERROR]") || l.includes("[CRITICAL]")) {
                            div.style.color = "#f87171";
                        } else if (l.includes("[SUCCESS]")) {
                            div.style.color = "#4ade80";
                        } else {
                            div.style.color = "#a7f3d0";
                        }
                        div.innerText = l;
                        gooseLogContainer.appendChild(div);
                    });
                    gooseLogContainer.scrollTop = gooseLogContainer.scrollHeight;
                }
            }
            
            // --- Home Page UI Updates ---
            const h = data.system_health;
            if (h) {
                window.latestTelemetryData = h;
                
                // Update deviceHeartbeats from real system health telemetry
                if (h.rtx_host) deviceHeartbeats.rtx_host.status = h.rtx_host.status;
                if (h.nas) deviceHeartbeats.nas.status = h.nas.status;
                if (h.pcloud) deviceHeartbeats.pcloud.status = h.pcloud.status === "CONNECTED" ? "ONLINE" : "OFFLINE";
                if (h.cloud_hq) deviceHeartbeats.cloud_hq.status = h.cloud_hq.status.includes("ACTIVE") ? "ONLINE" : "OFFLINE";
                if (h.telegram) deviceHeartbeats.telegram.status = h.telegram.status === "ACTIVE" ? "ONLINE" : "OFFLINE";

                if (typeof currentSlide !== 'undefined' && currentSlide >= 2) {
                    renderCarouselSlide(currentSlide);
                }
                // Update history queue for the live line graph
                const cpuVal = parseFloat(h.rtx_host.cpu);
                const gpuVal = parseFloat(h.rtx_host.gpu_temp);
                cpuHistory.push(isNaN(cpuVal) ? 22 : cpuVal);
                gpuHistory.push(isNaN(gpuVal) ? 61 : gpuVal);
                if (cpuHistory.length > 30) cpuHistory.shift();
                if (gpuHistory.length > 30) gpuHistory.shift();
                
                // Redraw chart
                drawTelemetryChart();
                // RTX Host
                const cpuEl = document.getElementById("rtx-cpu");
                const ramEl = document.getElementById("rtx-ram");
                const gpuEl = document.getElementById("rtx-gpu-temp");
                const vramEl = document.getElementById("rtx-vram");
                if (cpuEl) cpuEl.innerText = h.rtx_host.cpu;
                if (ramEl) ramEl.innerText = h.rtx_host.ram;
                if (gpuEl) gpuEl.innerText = h.rtx_host.gpu_temp;
                if (vramEl) vramEl.innerText = h.rtx_host.vram;
                
                // NAS
                const nasStorage = document.getElementById("nas-storage");
                const nasLatency = document.getElementById("nas-latency");
                if (nasStorage) nasStorage.innerText = h.nas.storage;
                if (nasLatency) nasLatency.innerText = h.nas.latency;
                
                // PCloud
                const indPcloud = document.getElementById("ind-pcloud");
                const pcloudStatus = document.getElementById("pcloud-status");
                const pcloudLatency = document.getElementById("pcloud-latency");
                const pcloudSync = document.getElementById("pcloud-sync");
                if (pcloudStatus) pcloudStatus.innerText = h.pcloud.status;
                if (pcloudLatency) pcloudLatency.innerText = h.pcloud.latency;
                if (pcloudSync) pcloudSync.innerText = h.pcloud.sync_state;
                if (indPcloud) {
                    indPcloud.className = h.pcloud.status === "CONNECTED" ? "status-indicator online" : "status-indicator offline";
                }
                
                // Cloud HQ
                const indCloudHq = document.getElementById("ind-cloud-hq");
                const cloudHqStatus = document.getElementById("cloud-hq-status");
                const cloudHqSync = document.getElementById("cloud-hq-sync");
                if (cloudHqStatus) cloudHqStatus.innerText = h.cloud_hq.status;
                if (cloudHqSync) cloudHqSync.innerText = h.cloud_hq.last_sync;
                if (indCloudHq) {
                    indCloudHq.className = data.is_cloud_active ? "status-indicator online" : "status-indicator online";
                }
                
                // Dashboard
                const dashUptime = document.getElementById("dash-uptime");
                const dashThreads = document.getElementById("dash-threads");
                if (dashUptime) dashUptime.innerText = h.dashboard.uptime;
                if (dashThreads) dashThreads.innerText = h.dashboard.threads;
                
                // Telegram
                const indTelegram = document.getElementById("ind-telegram");
                const tgStatusVal = document.getElementById("tg-status");
                const tgChat = document.getElementById("tg-chat");
                if (tgStatusVal) tgStatusVal.innerText = h.telegram.status;
                if (tgChat) tgChat.innerText = h.telegram.chat_id || "N/A";
                if (indTelegram) {
                    indTelegram.className = h.telegram.status === "ACTIVE" ? "status-indicator online" : "status-indicator offline";
                }
            }

            // --- Home Alarm Banner ---
            const homeAlarmBanner = document.getElementById("home-alarm-banner");
            const alarmDesc = document.getElementById("alarm-desc");
            const isAbnormal = data.blocked_scripts.length > 0 || !data.tg_active || data.last_sync_time === "N/A";
            
            if (homeAlarmBanner) {
                if (isAbnormal) {
                    homeAlarmBanner.style.display = "flex";
                    homeAlarmBanner.style.animation = "bannerPulse 1.5s infinite alternate";
                    let reason = [];
                    if (data.blocked_scripts.length > 0) reason.push(`[Sandbox] Blocked script ${data.blocked_scripts[0].brick}`);
                    if (!data.tg_active) reason.push(`[Telegram] Remote link offline`);
                    if (data.last_sync_time === "N/A") reason.push(`[Sync] Cloud handshake offline`);
                    if (alarmDesc) alarmDesc.innerText = reason.join(" | ");
                } else {
                    homeAlarmBanner.style.display = "none";
                }
            }

            // --- R&D Progress Lists & Bar ---
            const completedCount = data.completed_today ? data.completed_today.length : 0;
            const pendingCount = data.pending_tasks ? data.pending_tasks.length : 0;
            const totalCount = completedCount + pendingCount;
            const progressPercent = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0;
            
            const progressPercentEl = document.getElementById("dev-progress-percent");
            const progressBarEl = document.getElementById("dev-progress-bar");
            if (progressPercentEl) progressPercentEl.innerText = `${progressPercent}%`;
            if (progressBarEl) progressBarEl.style.width = `${progressPercent}%`;

            const homePendingList = document.getElementById("home-pending-list");
            const homeCompletedList = document.getElementById("home-completed-list");
            
            if (homePendingList) {
                homePendingList.innerHTML = "";
                if (pendingCount === 0) {
                    homePendingList.innerHTML = `<li style="color: var(--text-dim);">${currentLang === "zh" ? "無進行中任務" : "No active tasks"}</li>`;
                } else {
                    data.pending_tasks.forEach(t => {
                        const li = document.createElement("li");
                        li.style.color = "#fbbf24";
                        li.innerHTML = `⏳ <strong>${t.task_id}</strong>: ${escapeHTML(t.brick)} <span style="font-size: 9px; opacity: 0.8;">(${t.status})</span>`;
                        homePendingList.appendChild(li);
                    });
                }
            }
            
            if (homeCompletedList) {
                homeCompletedList.innerHTML = "";
                if (completedCount === 0) {
                    homeCompletedList.innerHTML = `<li style="color: var(--text-dim);">${currentLang === "zh" ? "今日尚無完成項目" : "No tasks completed today"}</li>`;
                } else {
                    data.completed_today.forEach(t => {
                        const li = document.createElement("li");
                        li.style.color = "#10b981";
                        li.innerHTML = `✅ <strong>${t.task_id}</strong>: ${escapeHTML(t.brick)}`;
                        homeCompletedList.appendChild(li);
                    });
                }
            }

            // --- Doctor Healing Logs ---
            const homeDoctorLogs = document.getElementById("home-doctor-logs");
            const doctorStatusBadge = document.getElementById("doctor-status-badge");
            
            if (doctorStatusBadge) {
                if (data.doctor_active) {
                    doctorStatusBadge.innerText = currentLang === "zh" ? "監護中" : "MONITORING";
                    doctorStatusBadge.style.background = "#10b981";
                } else {
                    doctorStatusBadge.innerText = currentLang === "zh" ? "未啟動" : "INACTIVE";
                    doctorStatusBadge.style.background = "#ef4444";
                }
            }
            
            if (homeDoctorLogs) {
                homeDoctorLogs.innerHTML = "";
                if (!data.doctor_logs || data.doctor_logs.length === 0) {
                    homeDoctorLogs.innerHTML = `<div style="color: #888;">${currentLang === "zh" ? "尚無派遣與自癒紀錄。系統安全。" : "No doctor dispatch history. System safe."}</div>`;
                } else {
                    data.doctor_logs.forEach(l => {
                        const div = document.createElement("div");
                        if (l.includes("[ERROR]") || l.includes("FAILED")) {
                            div.style.color = "#f87171";
                        } else if (l.includes("SUCCESS") || l.includes("自癒")) {
                            div.style.color = "#4ade80";
                        } else {
                            div.style.color = "#a7f3d0";
                        }
                        div.innerText = l;
                        homeDoctorLogs.appendChild(div);
                    });
                    homeDoctorLogs.scrollTop = homeDoctorLogs.scrollHeight;
                }
            }

            // 5. Render Blocked Sandbox Scripts Table
            blockedScriptsTableBody.innerHTML = "";
            let targetTask = null;

            if (data.blocked_scripts.length === 0) {
                blockedScriptsTableBody.innerHTML = `
                    <tr>
                        <td colspan="4" style="text-align: center; color: var(--text-dim);">${currentLang === "zh" ? "無阻斷紀錄。系統安全。" : "No blocked scripts found. System secure."}</td>
                    </tr>`;
            } else {
                data.blocked_scripts.forEach(s => {
                    const tr = document.createElement("tr");
                    tr.style.cursor = "pointer";
                    tr.innerHTML = `
                        <td>${s.task_id}</td>
                        <td style="color: #f87171;">${escapeHTML(s.brick)}</td>
                        <td>${s.timestamp}</td>
                        <td style="color: #ef4444; font-weight: bold;">BLOCKED</td>
                    `;
                    
                    const blockTaskObj = {
                        task_id: s.task_id,
                        status: "BLOCKED_BY_SANDBOX",
                        instruction: JSON.stringify({ brick: s.brick }),
                        timestamp: s.timestamp
                    };
                    
                    tr.addEventListener("click", () => {
                        activeFlowTaskId = s.task_id;
                        renderTaskFlow(blockTaskObj);
                    });
                    
                    if (activeFlowTaskId === s.task_id) {
                        targetTask = blockTaskObj;
                    }
                    
                    blockedScriptsTableBody.appendChild(tr);
                });
            }

            // 6. Render Pending Approvals Table
            const approvalsRes = await fetch("/api/pending-approvals");
            if (approvalsRes.status === 200) {
                const approvals = await approvalsRes.json();
                approvalsTableBody.innerHTML = "";
                if (approvals.length === 0) {
                    approvalsTableBody.innerHTML = `
                        <tr>
                            <td colspan="4" style="text-align: center; color: var(--text-dim);">${currentLang === "zh" ? "無待核准任務。系統空閒。" : "No tasks awaiting supervisor approval. System idle."}</td>
                        </tr>`;
                } else {
                    approvals.forEach(a => {
                        const tr = document.createElement("tr");
                        tr.style.cursor = "pointer";
                        
                        let instData = "";
                        try {
                            const parsed = JSON.parse(a.instruction);
                            if (parsed.code) {
                                instData = `Draft Code: ${parsed.brick}`;
                            } else {
                                instData = `Run Brick: ${parsed.brick}`;
                            }
                        } catch (e) {
                            instData = a.instruction;
                        }

                        tr.innerHTML = `
                            <td>${a.task_id}</td>
                            <td style="color: #fbbf24; font-weight: bold;">${escapeHTML(instData)}</td>
                            <td>${a.timestamp}</td>
                            <td>
                                <button class="btn-action btn-approve" data-id="${a.task_id}" style="background: #10b981; color: white; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer; font-size: 0.8rem; margin-right: 5px; font-weight: bold;" data-i18n="status-connected">Approve</button>
                                <button class="btn-action btn-reject" data-id="${a.task_id}" style="background: #ef4444; color: white; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer; font-size: 0.8rem; font-weight: bold;" data-i18n="status-disconnected">Reject</button>
                            </td>
                        `;
                        
                        tr.querySelector(".btn-approve").addEventListener("click", (e) => {
                            e.stopPropagation();
                            approveTask(a.task_id);
                        });
                        tr.querySelector(".btn-reject").addEventListener("click", (e) => {
                            e.stopPropagation();
                            rejectTask(a.task_id);
                        });
                        
                        tr.addEventListener("click", (e) => {
                            if (!e.target.classList.contains("btn-action")) {
                                activeFlowTaskId = a.task_id;
                                renderTaskFlow(a);
                            }
                        });
                        
                        if (activeFlowTaskId === a.task_id) {
                            targetTask = a;
                        }
                        
                        approvalsTableBody.appendChild(tr);
                    });
                    
                    if (!targetTask && approvals.length > 0) {
                        targetTask = approvals[0];
                        activeFlowTaskId = targetTask.task_id;
                    }
                }
                
                // Render selected task flow diagram
                if (targetTask) {
                    renderTaskFlow(targetTask);
                } else if (data.blocked_scripts.length > 0 && !activeFlowTaskId) {
                    // Fallback to first blocked script
                    const firstBlock = data.blocked_scripts[0];
                    activeFlowTaskId = firstBlock.task_id;
                    renderTaskFlow({
                        task_id: firstBlock.task_id,
                        status: "BLOCKED_BY_SANDBOX",
                        instruction: JSON.stringify({ brick: firstBlock.brick }),
                        timestamp: firstBlock.timestamp
                    });
                } else if (approvals.length === 0 && data.blocked_scripts.length === 0) {
                    if (taskFlowViz) taskFlowViz.style.display = "none";
                }
            }
        } catch (err) {
            console.error("Failed to fetch cloud/approval status:", err);
        }
    }

    // Setup real-time SSE listener for background QC events
    function connectQCSocket() {
        const source = new EventSource("/api/qc-events");
        
        source.onmessage = function(event) {
            try {
                const qcData = JSON.parse(event.data);
                console.log("[SSE] Received background QC update:", qcData);
                
                if (qcData.status === "CHAT_PUSH") {
                    appendBubble(qcData.message.sender, qcData.message.text);
                    return;
                }
                
                const homeDoctorLogs = document.getElementById("home-doctor-logs");
                if (homeDoctorLogs) {
                    const div = document.createElement("div");
                    if (qcData.status === "SOFT_ALARM") {
                        div.style.color = "#f59e0b"; // Orange soft alarm warning
                        div.innerHTML = `⚠️ <strong>[QC SOFT ALARM]</strong> Action <code>${escapeHTML(qcData.action_id)}</code> flagged! RPN is ${qcData.rpn} (Threshold: 100). Execution flow unaffected.`;
                        
                        // Pulse the home alarm banner as warning
                        const homeAlarmBanner = document.getElementById("home-alarm-banner");
                        const alarmDesc = document.getElementById("alarm-desc");
                        if (homeAlarmBanner) {
                            homeAlarmBanner.style.display = "flex";
                            homeAlarmBanner.style.animation = "bannerPulse 1.5s infinite alternate";
                            if (alarmDesc) {
                                alarmDesc.innerText = `[QC SOFT ALARM] Action ${qcData.action_id} RPN is ${qcData.rpn} (High risk)`;
                            }
                        }
                    } else if (qcData.status === "HOOK_UPDATE") {
                        div.style.color = "#60a5fa"; // Light Blue
                        div.innerHTML = `📡 <strong>[HOOK UPDATE]</strong> Brick <code>${escapeHTML(qcData.action_id)}</code>: ${escapeHTML(qcData.details)}`;
                    } else {
                        div.style.color = "#34d399"; // Green success
                        div.innerHTML = `✅ <strong>[QC PASSED]</strong> Action <code>${escapeHTML(qcData.action_id)}</code> passed safety check (RPN: ${qcData.rpn}).`;
                    }
                    homeDoctorLogs.appendChild(div);
                    homeDoctorLogs.scrollTop = homeDoctorLogs.scrollHeight;
                }
            } catch (err) {
                console.error("[SSE] Failed to parse SSE event payload:", err);
            }
        };
        
        source.onerror = function() {
            source.close();
            setTimeout(connectQCSocket, 5000);
        };
    }

    // Remote Command Event Listeners
    const btnRemoteRetry = document.getElementById("btn-remote-retry");
    const btnRemoteRestart = document.getElementById("btn-remote-restart");
    
    if (btnRemoteRetry) {
        btnRemoteRetry.addEventListener("click", async () => {
            if (!confirm("確定要執行遠端任務重試嗎？")) return;
            addLogLine("info", "發送遠端指令：任務重試...");
            try {
                const res = await fetch("/api/remote-command", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ command: "TASK_RETRY" })
                });
                const data = await res.json();
                if (data.status === "success") {
                    addLogLine("success", `[Remote Command] 重試任務分派成功！`);
                } else {
                    addLogLine("error", `[Remote Command] 失敗：${data.message}`);
                }
            } catch (err) {
                addLogLine("error", `[Remote Command] 連線錯誤：${err.message}`);
            }
        });
    }
    
    if (btnRemoteRestart) {
        btnRemoteRestart.addEventListener("click", async () => {
            if (!confirm("確定要執行遠端緊急重啟嗎？這將重置所有背景進程！")) return;
            addLogLine("info", "發送遠端指令：緊急重啟...");
            try {
                const res = await fetch("/api/remote-command", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ command: "EMERGENCY_RESTART" })
                });
                const data = await res.json();
                if (data.status === "success") {
                    addLogLine("success", `[Remote Command] 緊急重啟訊號已成功派發！`);
                } else {
                    addLogLine("error", `[Remote Command] 失敗：${data.message}`);
                }
            } catch (err) {
                addLogLine("error", `[Remote Command] 連線錯誤：${err.message}`);
            }
        });
    }

    // --- Dynamic Carousel Board Engine & Heartbeat Fault Simulation ---
    let currentSlide = 0;
    const totalSlides = 8;
    let progressTimer = null;
    let progressPercent = 0;

    let deviceHeartbeats = {
        rtx_host: { name: "RTX3060 運算主機", robot: "RTX 算力核心守護神 (RTX Core Guardian)", status: "ONLINE" },
        nas: { name: "NAS 儲存中心", robot: "NAS 數據備份與磁碟陣列修復者 (NAS Storage Healer)", status: "ONLINE" },
        pcloud: { name: "Pcloud 網路網關", robot: "PCloud 隧道自癒維護器 (PCloud Tunnel Maintainer)", status: "ONLINE" },
        cloud_hq: { name: "雲端指揮部", robot: "雲端指揮雙活代理人 (Cloud HQ Sync Agent)", status: "ONLINE" },
        telegram: { name: "Telegram 遠端模組", robot: "Telegram 訊息網關重啟程式 (TG Gateway Watchdog)", status: "ONLINE" }
    };

    function renderCarouselSlide(index) {
        const wrapper = document.getElementById("carousel-board-wrapper");
        if (!wrapper) return;

        let html = "";
        const h = window.latestTelemetryData || {
            rtx_host: { cpu: "24%", ram: "48%", gpu_temp: "62°C", vram: "5.2 GB / 12 GB", fan: "45%" },
            nas: { storage: "4.2 TB / 16 TB", latency: "2ms" },
            pcloud: { status: "CONNECTED", latency: "14ms", sync_state: "Synced" },
            cloud_hq: { status: "STANDBY (LOCAL)", last_sync: "N/A" },
            telegram: { status: "ACTIVE", chat_id: "N/A" }
        };

        // Update dots UI
        const dotsContainer = document.getElementById("carousel-dots-container");
        if (dotsContainer) {
            dotsContainer.innerHTML = "";
            for (let i = 0; i < totalSlides; i++) {
                const dot = document.createElement("div");
                dot.className = `carousel-dot ${i === index ? "active" : ""}`;
                dot.title = `Slide ${i + 1}`;
                dot.addEventListener("click", () => {
                    selectSlide(i);
                });
                dotsContainer.appendChild(dot);
            }
        }

        if (index === 0) {
            // Slide 1: 今日進行專案
            const projects = [
                { name: "四合一架構", progress: 92, eta: "2026-07-28" },
                { name: "金融家專案", progress: 78, eta: "2026-08-05" },
                { name: "五隻母雞企劃案", progress: 45, eta: "2026-08-20" },
                { name: "一人公司專案", progress: 60, eta: "2026-08-15" },
                { name: "AG 2.0萬用Skills產生器", progress: 85, eta: "2026-07-30" }
            ];

            html = `
                <div class="carousel-card">
                    <div class="carousel-card-header">
                        <span class="carousel-card-title">🚀 今日進行專案 (Today's Projects)</span>
                        <span class="carousel-status-badge online">${currentLang === "zh" ? "進行中" : "ACTIVE"}</span>
                    </div>
                    <div class="carousel-list-container">
                        ${projects.map(p => `
                            <div class="carousel-list-item">
                                <div class="item-info">
                                    <strong>${p.name}</strong>
                                </div>
                                <div class="item-progress-wrapper">
                                    <div class="item-progress-bar">
                                        <div class="item-progress-fill" style="width: ${p.progress}%"></div>
                                    </div>
                                    <span style="font-weight:bold; font-size:11px;">${p.progress}%</span>
                                </div>
                                <span class="item-eta">${currentLang === "zh" ? "預估完工:" : "ETA:"} ${p.eta}</span>
                            </div>
                        `).join("")}
                    </div>
                </div>
            `;
        }
        else if (index === 1) {
            // Slide 2: 今日維修工程
            const operations = [
                { name: "ClawLibrary 埠口重啟與自癒調校", progress: 100, eta: "已完成" },
                { name: "Ollama AI 算力核心檢修", progress: 100, eta: "已完成" },
                { name: "NAS 鏡像磁碟備份同步", progress: 85, eta: "進行中" }
            ];
            html = `
                <div class="carousel-card">
                    <div class="carousel-card-header">
                        <span class="carousel-card-title">🩺 今日維修工程 (Today's Maintenance)</span>
                        <span class="carousel-status-badge online">${currentLang === "zh" ? "安全監控中" : "SECURE"}</span>
                    </div>
                    <div class="carousel-list-container">
                        ${operations.map(o => `
                            <div class="carousel-list-item">
                                <div class="item-info">
                                    <strong>${o.name}</strong>
                                </div>
                                <div class="item-progress-wrapper">
                                    <div class="item-progress-bar">
                                        <div class="item-progress-fill" style="width: ${o.progress}%; background: linear-gradient(90deg, #f59e0b, #ffb300);"></div>
                                    </div>
                                    <span style="font-weight:bold; font-size:11px;">${o.progress}%</span>
                                </div>
                                <span class="item-eta" style="color: ${o.progress === 100 ? "#10b981" : "#f59e0b"}; font-weight: bold;">${o.eta}</span>
                            </div>
                        `).join("")}
                    </div>
                </div>
            `;
        }
        else if (index === 2) {
            // Slide 3: RTX3060 Host
            const dev = deviceHeartbeats.rtx_host;
            const isOnline = dev.status === "ONLINE";
            html = `
                <div class="carousel-card">
                    <div class="carousel-card-header">
                        <span class="carousel-card-title">🖥️ RTX3060 運算主機 <span class="heartbeat-dot ${isOnline ? "" : "offline"}"></span></span>
                        <span class="carousel-status-badge ${dev.status.toLowerCase()}">${dev.status === "ONLINE" ? "線上健康" : (dev.status === "REPAIRING" ? "修補中" : "心跳斷線")}</span>
                    </div>
                    <div class="carousel-grid-metrics">
                        <div class="carousel-metric-card">
                            <span class="label">CPU 負載</span>
                            <span class="value">${isOnline ? h.rtx_host.cpu : "--%"}</span>
                        </div>
                        <div class="carousel-metric-card">
                            <span class="label">RAM 佔用</span>
                            <span class="value">${isOnline ? h.rtx_host.ram : "--%"}</span>
                        </div>
                        <div class="carousel-metric-card">
                            <span class="label">GPU 溫度</span>
                            <span class="value">${isOnline ? h.rtx_host.gpu_temp : "--°C"}</span>
                        </div>
                        <div class="carousel-metric-card">
                            <span class="label">顯存 VRAM</span>
                            <span class="value">${isOnline ? h.rtx_host.vram : "-- / --"}</span>
                        </div>
                        <div class="carousel-metric-card">
                            <span class="label">風扇轉速</span>
                            <span class="value">${isOnline ? h.rtx_host.fan : "--%"}</span>
                        </div>
                        <div class="carousel-metric-card">
                            <span class="label">維修守護</span>
                            <span class="value" style="font-size:10px; color:#6366f1;">${dev.robot}</span>
                        </div>
                    </div>
                </div>
            `;
        }
        else if (index === 3) {
            // Slide 4: NAS Host
            const dev = deviceHeartbeats.nas;
            const isOnline = dev.status === "ONLINE";
            html = `
                <div class="carousel-card">
                    <div class="carousel-card-header">
                        <span class="carousel-card-title">💾 NAS 儲存主機 <span class="heartbeat-dot ${isOnline ? "" : "offline"}"></span></span>
                        <span class="carousel-status-badge ${dev.status.toLowerCase()}">${dev.status === "ONLINE" ? "線上健康" : (dev.status === "REPAIRING" ? "修補中" : "心跳斷線")}</span>
                    </div>
                    <div class="carousel-grid-metrics">
                        <div class="carousel-metric-card">
                            <span class="label">容量狀態</span>
                            <span class="value">${isOnline ? h.nas.storage : "--"}</span>
                        </div>
                        <div class="carousel-metric-card">
                            <span class="label">連線延遲</span>
                            <span class="value">${isOnline ? h.nas.latency : "--ms"}</span>
                        </div>
                        <div class="carousel-metric-card">
                            <span class="label">磁碟健康</span>
                            <span class="value">${isOnline ? "NORMAL" : "OFFLINE"}</span>
                        </div>
                        <div class="carousel-metric-card">
                            <span class="label">陣列狀態</span>
                            <span class="value">${isOnline ? "RAID-5 OK" : "ARRAY ERROR"}</span>
                        </div>
                        <div class="carousel-metric-card">
                            <span class="label">維修守護</span>
                            <span class="value" style="font-size:10px; color:#6366f1;">${dev.robot}</span>
                        </div>
                    </div>
                </div>
            `;
        }
        else if (index === 4) {
            // Slide 5: Pcloud Host
            const dev = deviceHeartbeats.pcloud;
            const isOnline = dev.status === "ONLINE";
            html = `
                <div class="carousel-card">
                    <div class="carousel-card-header">
                        <span class="carousel-card-title">🌐 Pcloud 雲端網關 <span class="heartbeat-dot ${isOnline ? "" : "offline"}"></span></span>
                        <span class="carousel-status-badge ${dev.status.toLowerCase()}">${dev.status === "ONLINE" ? "已連線" : (dev.status === "REPAIRING" ? "修補中" : "心跳斷線")}</span>
                    </div>
                    <div class="carousel-grid-metrics">
                        <div class="carousel-metric-card">
                            <span class="label">連線狀態</span>
                            <span class="value">${isOnline ? h.pcloud.status : "OFFLINE"}</span>
                        </div>
                        <div class="carousel-metric-card">
                            <span class="label">同步延遲</span>
                            <span class="value">${isOnline ? h.pcloud.latency : "--ms"}</span>
                        </div>
                        <div class="carousel-metric-card">
                            <span class="label">對齊模式</span>
                            <span class="value">${isOnline ? h.pcloud.sync_state : "--"}</span>
                        </div>
                        <div class="carousel-metric-card">
                            <span class="label">同步隧道</span>
                            <span class="value">${isOnline ? "SECURE TUNNEL" : "TUNNEL BROKEN"}</span>
                        </div>
                        <div class="carousel-metric-card">
                            <span class="label">維修守護</span>
                            <span class="value" style="font-size:10px; color:#6366f1;">${dev.robot}</span>
                        </div>
                    </div>
                </div>
            `;
        }
        else if (index === 5) {
            // Slide 6: Cloud HQ
            const dev = deviceHeartbeats.cloud_hq;
            const isOnline = dev.status === "ONLINE";
            html = `
                <div class="carousel-card">
                    <div class="carousel-card-header">
                        <span class="carousel-card-title">☁️ 雲端指揮部連線 <span class="heartbeat-dot ${isOnline ? "" : "offline"}"></span></span>
                        <span class="carousel-status-badge ${dev.status.toLowerCase()}">${dev.status === "ONLINE" ? "線上健康" : (dev.status === "REPAIRING" ? "修補中" : "心跳斷線")}</span>
                    </div>
                    <div class="carousel-grid-metrics">
                        <div class="carousel-metric-card">
                            <span class="label">指揮接管</span>
                            <span class="value">${isOnline ? h.cloud_hq.status : "OFFLINE"}</span>
                        </div>
                        <div class="carousel-metric-card">
                            <span class="label">最後同步時間</span>
                            <span class="value" style="font-size: 11px;">${isOnline ? h.cloud_hq.last_sync : "--"}</span>
                        </div>
                        <div class="carousel-metric-card">
                            <span class="label">雙活機制</span>
                            <span class="value">${isOnline ? "ENABLED" : "DISABLED"}</span>
                        </div>
                        <div class="carousel-metric-card">
                            <span class="label">遠端代理人</span>
                            <span class="value" style="font-size:10px; color:#6366f1;">${dev.robot}</span>
                        </div>
                    </div>
                </div>
            `;
        }
        else if (index === 6) {
            // Slide 7: Telegram
            const dev = deviceHeartbeats.telegram;
            const isOnline = dev.status === "ONLINE";
            html = `
                <div class="carousel-card">
                    <div class="carousel-card-header">
                        <span class="carousel-card-title">🤖 Telegram 連線模組 <span class="heartbeat-dot ${isOnline ? "" : "offline"}"></span></span>
                        <span class="carousel-status-badge ${dev.status.toLowerCase()}">${dev.status === "ONLINE" ? "線上健康" : (dev.status === "REPAIRING" ? "修補中" : "心跳斷線")}</span>
                    </div>
                    <div class="carousel-grid-metrics">
                        <div class="carousel-metric-card">
                            <span class="label">通訊模組狀態</span>
                            <span class="value">${isOnline ? h.telegram.status : "INACTIVE"}</span>
                        </div>
                        <div class="carousel-metric-card">
                            <span class="label">主管綁定 ID</span>
                            <span class="value">${isOnline ? h.telegram.chat_id : "N/A"}</span>
                        </div>
                        <div class="carousel-metric-card">
                            <span class="label">通訊網關</span>
                            <span class="value">${isOnline ? "READY" : "OFFLINE"}</span>
                        </div>
                        <div class="carousel-metric-card">
                            <span class="label">守護守護者</span>
                            <span class="value" style="font-size:10px; color:#6366f1;">${dev.robot}</span>
                        </div>
                    </div>
                </div>
            `;
        }
        else if (index === 7) {
            // Slide 8: AI Orchestrator Catalog
            const catalogData = window.latestAIIntelligenceData || {
                timestamp: "N/A",
                total_analyzed_modules: 0,
                ai_status: "STANDBY",
                modules_catalog: [],
                engine_details: {
                    langgraph_active: false,
                    prefect_monitored: false,
                    lightrag_grounded: false,
                    ruff_analyzer_active: false,
                    diskcache_hits: 0,
                    newly_compiled: 0
                }
            };

            const previewModules = catalogData.modules_catalog;
            const details = catalogData.engine_details || {};

            html = `
            <div class="carousel-card" style="background: rgba(99, 102, 241, 0.05); border-color: rgba(99, 102, 241, 0.25); min-height: 240px; display: flex; flex-direction: column;">
                <div class="carousel-card-header" style="padding-bottom: 5px; border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <span class="carousel-card-title" style="color: #a5b4fc; font-weight: bold; font-size: 13px;">🧠 AI 智慧編排與六大防禦工具鏈</span>
                    <span class="carousel-status-badge online" style="background: linear-gradient(135deg, #6366f1, #4f46e5); font-weight: bold; font-size: 9px; padding: 2px 6px;">智慧監控中</span>
                </div>
                
                <!-- Toolchain status badges -->
                <div style="display: flex; justify-content: space-around; font-size: 9px; color: #9ca3af; margin: 5px 0; background: rgba(0,0,0,0.2); padding: 4px; border-radius: 4px;">
                    <span>Ruff 🛡️ ${details.ruff_analyzer_active ? "✅" : "❌"}</span>
                    <span>Cache 🗄️ ${details.diskcache_hits ? "✅" : "✅"}</span>
                    <span>RAG 🕸️ ${details.lightrag_grounded ? "✅" : "❌"}</span>
                    <span>Prefect ⚙️ ${details.prefect_monitored ? "✅" : "❌"}</span>
                    <span>Graph 🧠 ${details.langgraph_active ? "✅" : "❌"}</span>
                </div>

                <div class="carousel-grid-metrics" style="margin-bottom: 6px; gap: 5px; display: grid; grid-template-columns: repeat(3, 1fr);">
                    <div class="carousel-metric-card" style="padding: 4px; text-align: center; background: rgba(255,255,255,0.01);">
                        <span class="label" style="font-size: 9px;">納管模組</span>
                        <span class="value" style="color: #60a5fa; font-size: 13px; font-weight: bold;">${catalogData.total_analyzed_modules} 支</span>
                    </div>
                    <div class="carousel-metric-card" style="padding: 4px; text-align: center; background: rgba(255,255,255,0.01);">
                        <span class="label" style="font-size: 9px;">快取命中</span>
                        <span class="value" style="color: #fbbf24; font-size: 13px; font-weight: bold;">${details.diskcache_hits || 0} 次</span>
                    </div>
                    <div class="carousel-metric-card" style="padding: 4px; text-align: center; background: rgba(255,255,255,0.01);">
                        <span class="label" style="font-size: 9px;">更新時間</span>
                        <span class="value" style="font-size: 9px; word-break: break-all;">${catalogData.timestamp ? catalogData.timestamp.split(" ")[1] : "N/A"}</span>
                    </div>
                </div>

                <!-- Scrollable list of modules -->
                <div class="carousel-list-container" style="display: flex; flex-direction: column; gap: 4px; font-size: 10px; flex: 1; overflow-y: auto; max-height: 120px; padding-right: 2px;">
                    ${previewModules.length === 0 ? 
                        `<div style="text-align:center; color:#6b7280; padding:10px;">正在讀取 AI 語意分析快取中...</div>` : 
                        previewModules.map(m => {
                            let readinessColor = "#10b981";
                            if (m.readiness_score < 90) readinessColor = "#fbbf24";
                            const depsStr = m.dependencies && m.dependencies.length > 0 ? m.dependencies.join(", ") : "None";
                            return `
                            <div style="background: rgba(255,255,255,0.02); padding: 4px 6px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.03); display: flex; flex-direction: column;">
                                <div style="display: flex; justify-content: space-between; align-items: center; cursor: pointer;" onclick="const d = this.nextElementSibling; d.style.display = d.style.display === 'none' ? 'block' : 'none';">
                                    <span style="font-weight: bold; color: #cbd5e1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 50%;">📄 ${m.file_name}</span>
                                    <span style="color: ${readinessColor}; font-weight: bold; font-size: 9px;">就緒: ${m.readiness_score}%</span>
                                </div>
                                <div class="module-details" style="display: none; padding-top: 4px; margin-top: 4px; border-top: 1px dashed rgba(255,255,255,0.05); color: #9ca3af; font-size: 9px;">
                                    <div style="margin: 2px 0;"><b>簡介:</b> ${m.short_description}</div>
                                    <div style="margin: 2px 0;"><b>情境:</b> ${m.ai_best_use_case}</div>
                                    <div style="margin: 2px 0; color: #818cf8;"><b>🕸️ 圖譜依賴 (LightRAG):</b> ${depsStr}</div>
                                    <div style="margin: 2px 0; color: #ef4444;"><b>🛡️ Ruff 警告數:</b> ${m.ruff_violations_count || 0}</div>
                                </div>
                            </div>
                            `;
                        }).join("")
                    }
                </div>
            </div>
            `;
        }


        wrapper.innerHTML = html;
    }

    function selectSlide(idx) {
        currentSlide = idx;
        renderCarouselSlide(currentSlide);
        resetProgressTimer();
    }

    function resetProgressTimer() {
        if (progressTimer) clearInterval(progressTimer);
        progressPercent = 0;

        const barFill = document.getElementById("carousel-timer-fill");
        if (barFill) barFill.style.width = "0%";

        progressTimer = setInterval(() => {
            progressPercent += (100 / 150); // 15 seconds (150 steps of 100ms)
            if (barFill) barFill.style.width = `${Math.min(progressPercent, 100)}%`;

            if (progressPercent >= 100) {
                currentSlide = (currentSlide + 1) % totalSlides;
                selectSlide(currentSlide);
            }
        }, 100);
    }

    // Heartbeat & Alarm simulation
    function runHeartbeatSimulation() {
        // Mock fault injection completely removed to avoid random faked data.
        // Heartbeats are now fetched directly from actual device telemetries.
    }

    // Connect Navigation Buttons
    const btnPrev = document.getElementById("btn-carousel-prev");
    const btnNext = document.getElementById("btn-carousel-next");
    if (btnPrev) {
        btnPrev.addEventListener("click", () => {
            currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
            selectSlide(currentSlide);
        });
    }
    if (btnNext) {
        btnNext.addEventListener("click", () => {
            currentSlide = (currentSlide + 1) % totalSlides;
            selectSlide(currentSlide);
        });
    }

    // ==========================================
    // Universal Skills Generator Integration
    // ==========================================
    const skillGenForm = document.getElementById("skill-gen-form");
    const skillsRepoBody = document.getElementById("skills-repo-body");
    const skillExecLogs = document.getElementById("skill-exec-logs");
    const btnSkillGenSubmit = document.getElementById("btn-skill-gen-submit");

    // Fetch and render generated skills
    async function fetchGeneratedSkills() {
        if (!skillsRepoBody) return;
        try {
            const res = await fetch("/api/list-skills");
            const data = await res.json();
            
            skillsRepoBody.innerHTML = "";
            if (data.length === 0) {
                skillsRepoBody.innerHTML = `
                    <tr>
                        <td colspan="5" style="text-align: center; color: var(--text-dim);">無已生成的技能。請從左側建立第一個技能！</td>
                    </tr>
                `;
                return;
            }

            data.forEach(skill => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${skill.id}</td>
                    <td style="color: #60a5fa; font-weight: 600;">${skill.platform}</td>
                    <td style="font-family: var(--font-code); color: #e5e7eb;">${skill.target}</td>
                    <td style="color: #9ca3af; font-size: 11px;">${skill.created_at}</td>
                    <td style="text-align: center;">
                        <button class="btn-action btn-view-skill" data-id="${skill.id}" style="background: rgba(59, 130, 246, 0.2); border: 1px solid #3b82f6; color: #93c5fd; padding: 4px 8px; border-radius: 4px; cursor: pointer; font-size: 0.75rem; margin-right: 5px;">👁️ 檢視</button>
                        <button class="btn-action btn-run-skill" data-id="${skill.id}" style="background: rgba(16, 185, 129, 0.2); border: 1px solid #10b981; color: #a7f3d0; padding: 4px 8px; border-radius: 4px; cursor: pointer; font-size: 0.75rem;">▶️ 執行</button>
                    </td>
                `;

                // Add event listeners
                tr.querySelector(".btn-view-skill").addEventListener("click", () => {
                    skillExecLogs.innerHTML = `<strong>[Code View - ${skill.target}]</strong>\n\n${escapeHTML(skill.code_content)}`;
                });

                tr.querySelector(".btn-run-skill").addEventListener("click", () => {
                    runGeneratedSkill(skill.id, skill.target);
                });

                skillsRepoBody.appendChild(tr);
            });
        } catch (err) {
            console.error("Failed to list skills:", err);
        }
    }

    // Run generated script
    async function runGeneratedSkill(skillId, name) {
        if (!skillExecLogs) return;
        skillExecLogs.innerHTML = `[System] 正在啟動執行技能: ${name} (ID: ${skillId})...\n`;
        try {
            const res = await fetch("/api/run-generated-skill", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ id: skillId })
            });
            const data = await res.json();
            if (data.status === "success") {
                skillExecLogs.innerHTML += `\n[Exit Code: ${data.exit_code}]\n\n--- Standard Output ---\n${escapeHTML(data.stdout)}\n\n--- Standard Error ---\n${escapeHTML(data.stderr)}`;
            } else {
                skillExecLogs.innerHTML += `\n❌ 執行失敗: ${data.message}`;
            }
        } catch (err) {
            skillExecLogs.innerHTML += `\n❌ 通訊錯誤: ${err}`;
        }
    }

    const skillSelectorList = document.getElementById("skill-selector-list");
    const brickSelectorList = document.getElementById("brick-selector-list");

    // Fetch and populate existing skills & bricks checklist
    async function loadExistingAssets() {
        if (!skillSelectorList || !brickSelectorList) return;
        try {
            const res = await fetch("/api/list-assets");
            const data = await res.json();
            
            // Render skills checkboxes
            skillSelectorList.innerHTML = "";
            if (!data.skills || data.skills.length === 0) {
                skillSelectorList.innerHTML = `<div style="color: var(--text-dim); text-align: center; padding: 5px;">無現有技能可搭配</div>`;
            } else {
                data.skills.forEach(skill => {
                    const label = document.createElement("label");
                    label.style.display = "flex";
                    label.style.alignItems = "center";
                    label.style.gap = "8px";
                    label.style.marginBottom = "4px";
                    label.style.cursor = "pointer";
                    label.innerHTML = `<input type="checkbox" name="selected_skills" value="${skill}"> <span style="font-family: var(--font-code); color: #93c5fd;">${skill}</span>`;
                    skillSelectorList.appendChild(label);
                });
            }

            // Render bricks checkboxes
            brickSelectorList.innerHTML = "";
            if (!data.bricks || data.bricks.length === 0) {
                brickSelectorList.innerHTML = `<div style="color: var(--text-dim); text-align: center; padding: 5px;">無現有積木可搭配</div>`;
            } else {
                data.bricks.forEach(brick => {
                    const label = document.createElement("label");
                    label.style.display = "flex";
                    label.style.alignItems = "center";
                    label.style.gap = "8px";
                    label.style.marginBottom = "4px";
                    label.style.cursor = "pointer";
                    label.innerHTML = `<input type="checkbox" name="selected_bricks" value="${brick}"> <span style="font-family: var(--font-code); color: #a7f3d0;">${brick}</span>`;
                    brickSelectorList.appendChild(label);
                });
            }
        } catch (err) {
            console.error("Failed to load assets:", err);
            skillSelectorList.innerHTML = `<div style="color: red; text-align: center; padding: 5px;">載入失敗</div>`;
            brickSelectorList.innerHTML = `<div style="color: red; text-align: center; padding: 5px;">載入失敗</div>`;
        }
    }

    // Handle form submission
    if (skillGenForm) {
        skillGenForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            
            const platform = document.getElementById("skill-platform").value;
            const target = document.getElementById("skill-target").value.trim();
            const specifications = document.getElementById("skill-specs").value.trim();
            const teamProfile = document.getElementById("skill-team") ? document.getElementById("skill-team").value : "None";
            
            const checkedSkills = Array.from(document.querySelectorAll("input[name='selected_skills']:checked")).map(el => el.value);
            const checkedBricks = Array.from(document.querySelectorAll("input[name='selected_bricks']:checked")).map(el => el.value);
            const attachmentFile = document.getElementById("skill-attachment").files[0];

            btnSkillGenSubmit.disabled = true;
            btnSkillGenSubmit.innerText = "⏳ AI 正在極速造物中...";
            if (skillExecLogs) {
                skillExecLogs.innerHTML = `[System] 已送出 AI 造物與承接請求...\n- 平台: ${platform}\n- 目標: ${target}\n- 規格: ${specifications}\n- 承接團隊: ${teamProfile}\n- 搭配技能: ${checkedSkills.join(', ') || '無'}\n- 搭配積木: ${checkedBricks.join(', ') || '無'}\n`;
            }

            const sendPayload = async (attachmentName = null, attachmentContent = null) => {
                const payload = {
                    platform,
                    target,
                    specifications,
                    team_profile: teamProfile,
                    selected_skills: checkedSkills,
                    selected_bricks: checkedBricks,
                    attachment_name: attachmentName,
                    attachment_content: attachmentContent
                };

                try {
                    const res = await fetch("/api/generate-skill", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify(payload)
                    });
                    const data = await res.json();
                    if (data.status === "success") {
                        if (skillExecLogs) {
                            skillExecLogs.innerHTML += `\n🎉 技能成功生成且承接配置完畢！已儲存至：\n${data.filepath}\n\n[自動載入代碼內容...]\n\n${escapeHTML(data.code)}`;
                        }
                        skillGenForm.reset();
                        fetchGeneratedSkills();
                        loadExistingAssets();
                    } else {
                        if (skillExecLogs) {
                            skillExecLogs.innerHTML += `\n❌ 生成與承接失敗: ${data.message}`;
                        }
                    }
                } catch (err) {
                    if (skillExecLogs) {
                        skillExecLogs.innerHTML += `\n❌ 網路通訊異常: ${err}`;
                    }
                } finally {
                    btnSkillGenSubmit.disabled = false;
                    btnSkillGenSubmit.innerText = "🚀 開始 AI 技能生成";
                }
            };

            if (attachmentFile) {
                if (skillExecLogs) {
                    skillExecLogs.innerHTML += `- 正在讀取附件: ${attachmentFile.name}...\n`;
                }
                const reader = new FileReader();
                reader.onload = function(evt) {
                    sendPayload(attachmentFile.name, evt.target.result);
                };
                reader.onerror = function() {
                    if (skillExecLogs) {
                        skillExecLogs.innerHTML += `\n[Warning] 讀取附件失敗，將在沒有附件的情況下繼續...\n`;
                    }
                    sendPayload();
                };
                reader.readAsText(attachmentFile);
            } else {
                sendPayload();
            }
        });
    }

    // Initialize Page
    // Adapt iframe sources to WAN/Tailscale remote hostnames dynamically
    const clawIframe = document.querySelector("#tab-clawlibrary iframe");
    if (clawIframe) {
        clawIframe.src = "http://" + window.location.hostname + ":5188/";
    }
    const nrIframe = document.querySelector("#tab-nodered iframe");
    if (nrIframe) {
        nrIframe.src = "http://" + window.location.hostname + ":1880/ui/";
    }

    applyLanguage(currentLang);
    fetchTree();
    pollTelemetry();
    fetchDFMEA();
    fetchGeneratedSkills();
    loadExistingAssets();
    pollLogs();
    pollCloudStatus();
    fetchAIIntelligence();
    async function fetchChatHistory() {
  try {
    const res = await fetch("/api/chat-history");
    if (res.status === 200) {
      const data = await res.json();
      const chatMessages = document.getElementById("chat-messages");
      if (!chatMessages) return;
      
      const existingBubbles = chatMessages.querySelectorAll(".message-bubble");
      if (existingBubbles.length !== data.length) {
        const typingBubble = chatMessages.querySelector(".typing");
        chatMessages.innerHTML = "";
        
        data.forEach(msg => {
          const bubble = document.createElement("div");
          bubble.className = `message-bubble ${msg.sender}`;
          const formattedText = msg.sender === "received" ? msg.text.replace(/\n/g, "<br>") : escapeHTML(msg.text);
          bubble.innerHTML = `<p>${formattedText}</p><span class="time">${msg.time}</span>`;
          chatMessages.appendChild(bubble);
        });
        
        if (typingBubble) {
          chatMessages.appendChild(typingBubble);
        }
        chatMessages.scrollTop = chatMessages.scrollHeight;
      }
    }
  } catch (err) {
    console.error("Failed to fetch chat history:", err);
  }
}

    fetchChatHistory();
    startAutoCycle();
    connectQCSocket();
    
    // Start carousel and heartbeat simulation
    selectSlide(0);
    runHeartbeatSimulation();
    
    // Set Intervals
    setInterval(pollTelemetry, 2000);
    setInterval(pollLogs, 2000);
    setInterval(fetchChatHistory, 5000);
    setInterval(pollCloudStatus, 5000);
    setInterval(fetchAIIntelligence, 10000);

    // ==========================================
    // Manual Switches & Override Control Handlers
    // ==========================================
    
    // 1. Watchdog Toggle
    const btnWatchdogToggle = document.getElementById("btn-watchdog-toggle");
    if (btnWatchdogToggle) {
        btnWatchdogToggle.addEventListener("click", async () => {
            try {
                const res = await fetch("/api/toggle-watchdog", { method: "POST" });
                const data = await res.json();
                if (data.status === "success") {
                    btnWatchdogToggle.innerText = data.enabled ? "🤖 自癒守護: ON" : "🤖 自癒守護: OFF";
                    btnWatchdogToggle.style.background = data.enabled ? "linear-gradient(135deg, #a855f7, #7e22ce)" : "#4b5563";
                    addLogLine("info", `Watchdog self-healing set to: ${data.enabled ? 'ON' : 'OFF'}`);
                }
            } catch (err) {
                addLogLine("error", `Failed to toggle watchdog: ${err.message}`);
            }
        });
    }

    // 2. Clear Orchestrator Cache
    const btnClearCache = document.getElementById("btn-clear-cache");
    if (btnClearCache) {
        btnClearCache.addEventListener("click", async () => {
            if (!confirm("確定要清除 AI 語意快取嗎？這會強制重新掃描代碼。")) return;
            try {
                const res = await fetch("/api/clear-cache", { method: "POST" });
                const data = await res.json();
                if (data.status === "success") {
                    addLogLine("success", "Orchestrator capability cache successfully cleared.");
                    fetchAIIntelligence();
    async function fetchChatHistory() {
  try {
    const res = await fetch("/api/chat-history");
    if (res.status === 200) {
      const data = await res.json();
      const chatMessages = document.getElementById("chat-messages");
      if (!chatMessages) return;
      
      const existingBubbles = chatMessages.querySelectorAll(".message-bubble");
      if (existingBubbles.length !== data.length) {
        const typingBubble = chatMessages.querySelector(".typing");
        chatMessages.innerHTML = "";
        
        data.forEach(msg => {
          const bubble = document.createElement("div");
          bubble.className = `message-bubble ${msg.sender}`;
          const formattedText = msg.sender === "received" ? msg.text.replace(/\n/g, "<br>") : escapeHTML(msg.text);
          bubble.innerHTML = `<p>${formattedText}</p><span class="time">${msg.time}</span>`;
          chatMessages.appendChild(bubble);
        });
        
        if (typingBubble) {
          chatMessages.appendChild(typingBubble);
        }
        chatMessages.scrollTop = chatMessages.scrollHeight;
      }
    }
  } catch (err) {
    console.error("Failed to fetch chat history:", err);
  }
}

    fetchChatHistory();
                }
            } catch (err) {
                addLogLine("error", `Failed to clear cache: ${err.message}`);
            }
        });
    }

    // 3. Trigger DFMEA Audit Scan
    const btnRunDfmeaAudit = document.getElementById("btn-run-dfmea-audit");
    if (btnRunDfmeaAudit) {
        btnRunDfmeaAudit.addEventListener("click", async () => {
            addLogLine("info", "Starting full quality control DFMEA safety scan...");
            try {
                const res = await fetch("/api/run-dfmea-audit", { method: "POST" });
                const data = await res.json();
                if (data.status === "success") {
                    addLogLine("success", `[DFMEA Audit] Result: ${data.message}`);
                    fetchDFMEA();
                } else {
                    addLogLine("error", `[DFMEA Audit] Failed: ${data.message}`);
                }
            } catch (err) {
                addLogLine("error", `Failed to trigger DFMEA audit: ${err.message}`);
            }
        });
    }

    // 4. Backup Database
    const btnDbBackup = document.getElementById("btn-db-backup");
    if (btnDbBackup) {
        btnDbBackup.addEventListener("click", () => triggerChatCommand("/backup"));
    }

    // 5. Clear Console Screen
    const btnClearConsole = document.getElementById("btn-clear-console");
    if (btnClearConsole) {
        btnClearConsole.addEventListener("click", () => {
            const consoleBox = document.getElementById("console-logs");
            if (consoleBox) {
                consoleBox.innerHTML = `<div class="log-line info">[INFO] Console logs screen cleared.</div>`;
            }
        });
    }

    // 6. Push Logs to Telegram
    const btnPushLogsTelegram = document.getElementById("btn-push-logs-telegram");
    if (btnPushLogsTelegram) {
        btnPushLogsTelegram.addEventListener("click", async () => {
            try {
                const res = await fetch("/api/push-logs-telegram", { method: "POST" });
                const data = await res.json();
                if (data.status === "success") {
                    addLogLine("success", "Recent console logs successfully pushed to Telegram owner.");
                }
            } catch (err) {
                addLogLine("error", `Failed to push logs: ${err.message}`);
            }
        });
    }

    // 7. Force Cloud Sync
    const btnForceCloudSync = document.getElementById("btn-force-cloud-sync");
    if (btnForceCloudSync) {
        btnForceCloudSync.addEventListener("click", async () => {
            addLogLine("info", "Forcing instant cloud-local synchronization heartbeat...");
            try {
                const res = await fetch("/api/force-cloud-sync", { method: "POST" });
                const data = await res.json();
                if (data.status === "success") {
                    addLogLine("success", "Cloud-local sync process completed successfully.");
                    pollCloudStatus();
                }
            } catch (err) {
                addLogLine("error", `Failed to run cloud sync: ${err.message}`);
            }
        });
    }

    // 8. Restart ClawLibrary Service
    const btnRestartClaw = document.getElementById("btn-restart-claw");
    if (btnRestartClaw) {
        btnRestartClaw.addEventListener("click", async () => {
            if (!confirm("確定要重啟 ClawLibrary 2D 服務嗎？")) return;
            addLogLine("info", "Dispatching restart request for ClawLibrary (Port 5188)...");
            try {
                const res = await fetch("/api/restart-service", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ service: "ClawLibrary" })
                });
                const data = await res.json();
                if (data.status === "success") {
                    addLogLine("success", "ClawLibrary service successfully restarted.");
                }
            } catch (err) {
                addLogLine("error", `Failed to restart ClawLibrary: ${err.message}`);
            }
        });
    }

    // 9. Restart Node-RED Service
    const btnRestartNodeRed = document.getElementById("btn-restart-nodered");
    if (btnRestartNodeRed) {
        btnRestartNodeRed.addEventListener("click", async () => {
            if (!confirm("確定要重啟 Node-RED 服務嗎？")) return;
            addLogLine("info", "Dispatching restart request for Node-RED (Port 1880)...");
            try {
                const res = await fetch("/api/restart-service", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ service: "Node-RED" })
                });
                const data = await res.json();
                if (data.status === "success") {
                    addLogLine("success", "Node-RED service successfully restarted.");
                }
            } catch (err) {
                addLogLine("error", `Failed to restart Node-RED: ${err.message}`);
            }
        });
    }

    // 10. Reload Assets Lists
    const btnReloadAssets = document.getElementById("btn-reload-assets");
    if (btnReloadAssets) {
        btnReloadAssets.addEventListener("click", () => {
            addLogLine("info", "Reloading workspace asset lists for generator...");
            loadExistingAssets();
        });
    }
});



function renderProjectorAIPanel() {
    const overlay = document.getElementById("projector-overlay-content");
    if (!overlay) return;
    
    const catalogData = window.latestAIIntelligenceData || {
        timestamp: "N/A",
        total_analyzed_modules: 0,
        ai_status: "STANDBY",
        modules_catalog: [],
        engine_details: {
            langgraph_active: false,
            prefect_monitored: false,
            lightrag_grounded: false,
            ruff_analyzer_active: false,
            diskcache_hits: 0,
            newly_compiled: 0
        }
    };
    
    const details = catalogData.engine_details || {};
    const modules = catalogData.modules_catalog || [];
    
    let html = `
    <div style="padding: 10px; font-family: 'Outfit', sans-serif;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid rgba(99, 102, 241, 0.3); padding-bottom: 6px; margin-bottom: 12px;">
            <span style="font-size: 14px; font-weight: bold; color: #a5b4fc; text-shadow: 0 0 8px rgba(99, 102, 241, 0.5);">🧬 AI Orchestration Codebase & Knowledge Graph Telemetry</span>
            <span style="font-size: 9px; color: #9ca3af; font-family: monospace;">HASH: 7d3f4181...</span>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 15px; height: 180px;">
            <!-- Left Panel: Engine status -->
            <div style="background: rgba(99, 102, 241, 0.05); border: 1px solid rgba(99, 102, 241, 0.2); padding: 8px; border-radius: 8px; font-size: 11px;">
                <div style="font-weight: bold; color: #60a5fa; margin-bottom: 6px; border-bottom: 1px dashed rgba(255,255,255,0.1); padding-bottom: 4px;">🛡️ 智慧核心防禦工具鏈</div>
                <div style="display: flex; flex-direction: column; gap: 4px;">
                    <div>• <b>Ruff 靜態分析:</b> ${details.ruff_analyzer_active ? "<span style='color:#10b981;'>ACTIVE ✅</span>" : "<span style='color:#ef4444;'>INACTIVE ❌</span>"}</div>
                    <div>• <b>DiskCache 快取:</b> <span style="color:#10b981;">命中 ${details.diskcache_hits || 0} 次 ✅</span></div>
                    <div>• <b>LightRAG 雙層關係:</b> ${details.lightrag_grounded ? "<span style='color:#10b981;'>GROUNDED ✅</span>" : "<span style='color:#ef4444;'>OFFLINE ❌</span>"}</div>
                    <div>• <b>Prefect 背景監控:</b> ${details.prefect_monitored ? "<span style='color:#10b981;'>RUNNING ✅</span>" : "<span style='color:#ef4444;'>OFFLINE ❌</span>"}</div>
                    <div>• <b>LangGraph 閉環編排:</b> ${details.langgraph_active ? "<span style='color:#10b981;'>ACTIVE ✅</span>" : "<span style='color:#ef4444;'>OFFLINE ❌</span>"}</div>
                    <div>• <b>最後同步更新:</b> <span style="color:#fbbf24;">${catalogData.timestamp || "N/A"}</span></div>
                </div>
            </div>
            
            <!-- Right Panel: Dynamic Module Graph List -->
            <div style="background: rgba(0, 0, 0, 0.3); border: 1px solid rgba(255, 255, 255, 0.05); padding: 8px; border-radius: 8px; display: flex; flex-direction: column; overflow: hidden;">
                <div style="font-weight: bold; color: #a5b4fc; margin-bottom: 6px; font-size: 11px; display: flex; justify-content: space-between;">
                    <span>📂 納管代碼實體與 RAG 依賴關係圖譜</span>
                    <span style="color: #60a5fa; font-size: 10px;">(共 ${catalogData.total_analyzed_modules} 個模組)</span>
                </div>
                <div style="flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 4px; padding-right: 4px;">
                    ${modules.length === 0 ? 
                        `<div style="color:#6b7280; text-align:center; padding-top:40px; font-size:11px;">無可用分析快取資料。請手動點擊「清除編排快取」或觸發分析管線。</div>` :
                        modules.map(m => {
                            let readinessColor = "#10b981";
                            if (m.readiness_score < 90) readinessColor = "#fbbf24";
                            const ruffBadge = m.ruff_violations_count > 0 ? `<span style="background:#ef4444; color:#fff; font-size:8px; padding:1px 3px; border-radius:2px; margin-left:5px;">Ruff: ${m.ruff_violations_count}</span>` : "";
                            const depsStr = m.dependencies && m.dependencies.length > 0 ? m.dependencies.join(", ") : "無依賴";
                            return `
                            <div style="background: rgba(255,255,255,0.02); padding: 4px 6px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.03); display: flex; justify-content: space-between; align-items: center; font-size: 10px;">
                                <div style="display: flex; flex-direction: column; max-width: 70%;">
                                    <span style="font-weight: bold; color: #cbd5e1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">📄 ${m.file_name}</span>
                                    <span style="font-size: 9px; color: #818cf8; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">🕸️ RAG: ${depsStr}</span>
                                </div>
                                <div style="text-align: right;">
                                    <span style="color: ${readinessColor}; font-weight: bold; font-size: 10px;">就緒: ${m.readiness_score}%</span>
                                    <div>${ruffBadge}</div>
                                </div>
                            </div>
                            `;
                        }).join("")
                    }
                </div>
            </div>
        </div>
    </div>
    `;
    
    overlay.innerHTML = html;
}
