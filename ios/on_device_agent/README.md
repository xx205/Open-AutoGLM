# iOS：把 Agent 逻辑跑在 WDA Runner（XCTest）里（手机端自循环，可在手机上配置）

这个目录提供一个 **实验性** 方案：把 AutoGLM 的闭环（截图 → 调 LLM → 解析动作 → 执行）塞进 `WebDriverAgentRunner-Runner`（`.xctrunner`）的测试进程里运行。

你不需要在电脑上运行 `python ios.py ...` 的循环；配置（`base_url/model/api_key/task` 等）可以在 iPhone 上直接填写，然后让 Runner 在手机上自己跑。

> 仍然需要 macOS + Xcode（至少一次）把 Runner 编译/安装到 iPhone 上；WDA/XCTest 才有跨 App 自动化能力。

---

## 你会得到什么

- 一个对 WebDriverAgent 的补丁：`ios/on_device_agent/patches/webdriveragent_autoglm_on_device_agent_webui.patch`
  - 增加一个手机端可访问的页面：`GET /autoglm`
  - 在该页面输入 `base_url/model/api_key/task`，点击 Start/Stop 即可
  - Agent 循环在 Runner 进程内执行：截图、调用 LLM、执行 tap/swipe/type 等

补丁会新增这些 endpoints（都挂在 WDA 的同一个 8100 端口上）：

- `GET /autoglm`：配置/启动页面（HTML）
- `GET /autoglm/status`：当前运行状态（JSON）
- `GET /autoglm/logs`：最近日志（JSON）
- `POST /autoglm/config`：保存配置（JSON body）
- `POST /autoglm/start`：保存配置并启动（JSON body）
- `POST /autoglm/stop`：停止（无需 body）

---

## 典型流程（推荐按这个）

### 0) 准备：先让 WDA 能跑起来

按你现有的 WDA 流程，用 Xcode 把 `WebDriverAgentRunner-Runner` 装到 iPhone 上并能启动 WDA。

并确认 iPhone 上：

`Settings -> Apps -> WebDriverAgentRunner-Runner -> Wireless Data` 不是 Off（选 WLAN 或 WLAN & Cellular Data）

否则 `http://<iphone-ip>:8100/...` 可能不可达（`127.0.0.1` 往往仍可达）。

### 1) 在一个“新的 WDA 目录”里应用补丁（避免改动你现有 WDA）

建议你复制/clone 一份新的 WebDriverAgent 目录（例如 `WebDriverAgent-AutoGLM`），只在这份上打补丁。

在该 WDA 目录中执行：

```bash
git apply <path-to-Open-AutoGLM>/ios/on_device_agent/patches/webdriveragent_autoglm_on_device_agent_webui.patch
```

### 2) 用 Xcode 重新安装一次 Runner

因为你修改了 WDA 源码，需要重新编译/安装一次 `WebDriverAgentRunner-Runner` 到 iPhone。

之后你只要不再改 WDA 代码，就不需要每次都重新装。

### 3) 启动 WDA（任意你顺手的方式）

你可以继续用：
- Xcode `Product -> Test`
- `xcodebuild ... test`
- `devicectl process launch ...`（如果你已经走“preinstalled Runner”的路线）

确保 WDA 已经在跑（`/status` 可访问）。

### 4) 在 iPhone 上直接配置并运行

在 iPhone 的 Safari 打开：

- `http://127.0.0.1:8100/autoglm`（推荐：不依赖 Wi‑Fi LAN 可达）

或（Wi‑Fi 可达时）：

- `http://<iphone-ip>:8100/autoglm`

在页面里填：
- `Base URL`（OpenAI-compatible，例如 `https://...` 或本地网关）
- `Model`
- `API Key`（如果你的服务需要）
- `Task`

然后点击 **Start**。

---

## 安全提醒（务必读）

- WDA 本身就是“远程控制手机”的能力：如果你的 `8100` 端口对局域网开放，任何能访问到的人都能操作你的手机。
- `/autoglm` 页面里会需要输入 `API key`。请不要把包含 key 的截图/日志直接贴公开论坛；必要时务必打码。
