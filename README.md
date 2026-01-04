# Open-AutoGLM

[Readme in English](README_en.md)

<div align="center">
<img src=resources/logo.svg width="20%"/>
</div>
<p align="center">
    👋 加入我们的 <a href="resources/WECHAT.md" target="_blank">微信</a> 社区
</p>
<p align="center">
    🎤 进一步在我们的产品 <a href="https://autoglm.zhipuai.cn/autotyper/" target="_blank">智谱 AI 输入法</a> 体验“用嘴发指令”
</p>

## 懒人版快速安装

你可以使用 Claude Code，配置 [GLM Coding Plan](https://bigmodel.cn/glm-coding) 后，输入以下提示词，快速部署本项目。

```
访问文档，为我安装 AutoGLM
https://raw.githubusercontent.com/zai-org/Open-AutoGLM/refs/heads/main/README.md
```

## 项目介绍

Phone Agent 是一个基于 AutoGLM 构建的手机端智能助理框架，它能够以多模态方式理解手机屏幕内容，并通过自动化操作帮助用户完成任务。系统通过
ADB (Android Debug Bridge) 来控制设备，以视觉语言模型进行屏幕感知，再结合智能规划能力生成并执行操作流程。用户只需用自然语言描述需求，如“打开小红书搜索美食”，Phone
Agent 即可自动解析意图、理解当前界面、规划下一步动作并完成整个流程。系统还内置敏感操作确认机制，并支持在登录或验证码场景下进行人工接管。同时，它提供远程
ADB 调试能力，可通过 WiFi 或网络连接设备，实现灵活的远程控制与开发。

> ⚠️
> 本项目仅供研究和学习使用。严禁用于非法获取信息、干扰系统或任何违法活动。请仔细审阅 [使用条款](resources/privacy_policy.txt)。

## 模型下载地址

| Model                         | Download Links                                                                                                                                                         |
|-------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| AutoGLM-Phone-9B              | [🤗 Hugging Face](https://huggingface.co/zai-org/AutoGLM-Phone-9B)<br>[🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/AutoGLM-Phone-9B)                           |
| AutoGLM-Phone-9B-Multilingual | [🤗 Hugging Face](https://huggingface.co/zai-org/AutoGLM-Phone-9B-Multilingual)<br>[🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/AutoGLM-Phone-9B-Multilingual) |

其中，`AutoGLM-Phone-9B` 是针对中文手机应用优化的模型，而 `AutoGLM-Phone-9B-Multilingual` 支持英语场景，适用于包含英文等其他语言内容的应用。

## Android 环境准备

### 1. Python 环境

建议使用 Python 3.10 及以上版本。

### 2. ADB (Android Debug Bridge)

1. 下载官方 ADB [安装包](https://developer.android.com/tools/releases/platform-tools?hl=zh-cn)，并解压到自定义路径
2. 配置环境变量

- MacOS 配置方法：在 `Terminal` 或者任何命令行工具里

  ```bash
  # 假设解压后的目录为 ~/Downloads/platform-tools。如果不是请自行调整命令。
  export PATH=${PATH}:~/Downloads/platform-tools
  ```

- Windows 配置方法：可参考 [第三方教程](https://blog.csdn.net/x2584179909/article/details/108319973) 进行配置。

### 3. Android 7.0+ 的设备或模拟器，并启用 `开发者模式` 和 `USB 调试`

1. 开发者模式启用：通常启用方法是，找到 `设置-关于手机-版本号` 然后连续快速点击 10
   次左右，直到弹出弹窗显示“开发者模式已启用”。不同手机会有些许差别，如果找不到，可以上网搜索一下教程。
2. USB 调试启用：启用开发者模式之后，会出现 `设置-开发者选项-USB 调试`，勾选启用
3. 部分机型在设置开发者选项以后, 可能需要重启设备才能生效. 可以测试一下: 将手机用 USB 数据线连接到电脑后, `adb devices`
   查看是否有设备信息, 如果没有说明连接失败.

**请务必仔细检查相关权限**

![权限](resources/screenshot-20251209-181423.png)

### 4. 安装 ADB Keyboard（用于文本输入）

下载 [安装包](https://github.com/senzhk/ADBKeyBoard/blob/master/ADBKeyboard.apk) 并在对应的安卓设备中进行安装。
注意，安装完成后还需要到 `设置-输入法` 或者 `设置-键盘列表` 中启用 `ADB Keyboard` 才能生效（或使用命令 `adb shell ime enable com.android.adbkeyboard/.AdbIME`，[How-to-use](https://github.com/senzhk/ADBKeyBoard/blob/master/README.md#how-to-use)）

## iPhone 环境准备

### 1. Python 环境

建议使用 Python 3.10 及以上版本。

### 2. 设置 WebDriverAgent

WebDriverAgent 是 iOS 自动化的核心组件，需要在 iOS 设备上运行。

注意：需要提前安装好 Xcode、并注册好苹果开发者账号（不需要付费）

#### 0. 背景：iOS 自动化里 WDA / Xcode / Runner 分别是什么

iOS 没有像 Android 那样通用的 ADB 入口。要在 iPhone 上做“点/滑/输入/截图”，通常需要走苹果的 **XCUITest**（Xcode 的 UI 自动化测试框架）。

WebDriverAgent（WDA）可以理解为：把 XCUITest 的能力封装成一个可通过 HTTP 调用的服务。AutoGLM iOS 版就是“发 HTTP 请求给 WDA”，由 WDA 在手机上执行触控/输入/截图。

这条链路的关系可以简化为：

`AutoGLM (Mac)  --HTTP-->  WDA (iPhone)  --XCUITest-->  iOS UI`

下面把几个最容易混淆的名词解释清楚：

- **WDA 是什么**
  - WDA 在 iPhone 上跑起来后，会对外提供一个 HTTP 服务（默认端口 `8100`，常用检查接口是 `/status`）。
  - 你看到的 `http://...:8100/status` 能不能访问，本质就是“WDA 是否在跑 + 你的电脑能不能连到它”。

- **Xcode 在这里做什么**
  - 负责把 WDA 编译、签名并安装到 iPhone 上（iOS 应用必须签名才能安装运行）。
  - 负责启动一段 UI Test，会话里会把 WDA 的服务跑起来。

- **Runner 是什么（为什么手机设置里会出现 `WebDriverAgentRunner-Runner`）**
  - `WebDriverAgentRunner-Runner` 是 Xcode 跑 UI Test 时生成/安装到手机上的 **测试 Runner App**（你会在 iPhone `设置 -> 应用` 里看到它）。
  - 它不是你在工程里手动创建的一个 Target；工程里你需要配置的是 `WebDriverAgentRunner` 这个 Target（尤其是签名和 `PRODUCT_BUNDLE_IDENTIFIER`）。
  - 文档里说的“已安装 Runner”，意思就是：手机上已经能看到 `WebDriverAgentRunner-Runner` 这个 App（通常说明你至少成功跑通过一次 `Product > Test`）。

- **WDA URL 是什么（你要传给 `ios.py --wda-url` 的值）**
  - 它就是“运行 AutoGLM 的机器访问 WDA 的入口地址”：
    - **Wi‑Fi 直连**：`http://<iphone-ip>:8100`（依赖局域网互访；并且 iPhone 上该 App 的 `Wireless Data` 不能是 Off）
    - **USB + 端口转发**：用 `iproxy 8100 8100` 转发后访问 `http://127.0.0.1:8100`（最稳，完全绕开路由器/局域网策略）

你可以把整个流程拆成两步：

1) 让 WDA 在 iPhone 上启动起来（Runner 在跑，端口 8100 在监听）  
2) 选择一种方式让电脑能连上它（Wi‑Fi 直连 或 `iproxy` 转发）

#### 1. 推荐完整流程（优先 Wi‑Fi 直连 + 日常不再跑 xcodebuild）

这条流程的目标是：**只用 Xcode 安装/签名一次**，后续通过 `devicectl` 启动已安装的 Runner，从而尽量避免 Runner 被反复安装/更新导致的权限开关复位。

##### 1.1 一次性准备：安装 Runner（首次必做）

1) 克隆 WebDriverAgent：

```bash
git clone https://github.com/appium/WebDriverAgent.git
cd WebDriverAgent
```
2) 在 Xcode 中打开 `WebDriverAgent.xcodeproj`，配置 Signing & Capabilities。

把 `WebDriverAgentRunner` 这个 Target 的 Bundle Identifier（`PRODUCT_BUNDLE_IDENTIFIER`）改成你自己的固定值（例如 `YOUR_NAME.WebDriverAgentRunner`），并尽量保持长期不变（避免 iOS 把它当成新 App 重装导致权限/开关重置）。

说明：你在 iPhone“设置 -> 应用”里看到的 `WebDriverAgentRunner-Runner` 并不是工程里的一个 Target，而是 Xcode 运行 UI Test 时自动生成/安装的 Runner App（通常基于 `WebDriverAgentRunner` 派生，名字会带 `-Runner`）。

3) 选择 `WebDriverAgentRunner` scheme 和你的 iPhone 设备，执行 `Product > Test`（或 `Cmd+U`）。

首次运行时，可能需要在 iPhone 上解锁并在 **设置 -> 通用 -> VPN 与设备管理** 中信任开发者 App。

你只需要确保能跑通一次：手机上出现 `WebDriverAgentRunner-Runner`，并且 WDA 能对外提供 `/status`。

可选：更可控地“安装/更新一次 Runner”（后续只用 devicectl 启动）

如果你希望把“安装/更新”单独做一次（后续只做启动/停止），或者你在 iOS 17+ / 18 上遇到 `devicectl` 启动后立刻退出等问题，可以按 `docs/recipes/run_wda_preinstalled_devicectl.md` 的步骤做一次可控安装。这里给出最小操作摘要：

1) 找到 Xcode 编译产物里的 Runner `.app`（通常在 DerivedData）：

```bash
ls ~/Library/Developer/Xcode/DerivedData/WebDriverAgent-*/Build/Products/Debug-iphoneos/WebDriverAgentRunner-Runner.app
```

2) （可选）准备一个“更适合 devicectl 启动”的 Runner（删除 `Frameworks/XC*.framework` 并重新签名）：

```bash
bash scripts/prepare_wda_runner_for_devicectl.sh \
  --app ~/Library/Developer/Xcode/DerivedData/WebDriverAgent-*/Build/Products/Debug-iphoneos/WebDriverAgentRunner-Runner.app \
  --out /tmp/WDA-Prepared
```

3) 安装到设备（只需做一次，后续不再安装）：

```bash
xcrun devicectl device install app --device <UDID> /tmp/WDA-Prepared/WebDriverAgentRunner-Runner.app
```

其中 `<UDID>` 可通过 `xcrun devicectl list devices` 获取（见下方 1.3）。

安装会覆盖/更新该 App，建议在安装完成后再按下面 1.2 把 `Wireless Data` 打开一次。

##### 1.2 一次性准备：让 Wi‑Fi 访问可用（否则 `<iphone-ip>:8100` 会超时）

如果你希望用 `http://<iphone-ip>:8100`（Wi‑Fi 直连），请务必检查 iPhone 上：

`设置 -> App（或 应用）-> WebDriverAgentRunner-Runner -> 无线数据（Wireless Data）`

把 **Off** 改成 **WLAN** 或 **WLAN & Cellular Data**。

> 这是一个非常容易踩坑的点：开关为 Off 时，你会看到 `http://127.0.0.1:8100/status` 在 iPhone 上可访问，但 `http://<iphone-ip>:8100/status`（甚至 iPhone 自己访问 `<iphone-ip>`）会 timeout。  
> 另外，如果你走的是“Wi‑Fi 连接运行 Xcode UI Test”，这个开关为 Off 也常见会导致设备日志出现 `Exiting due to IDE disconnection.`。

##### 1.3 日常启动：用 devicectl 启动“已安装的 Runner”（不再跑 xcodebuild）

1) 获取设备 UDID：

```bash
xcrun devicectl list devices
```

2) 获取 WDA `*.xctrunner` 的 bundle id（包含 `.xctrunner` 后缀）：

```bash
xcrun devicectl device info apps --device <UDID> --include-all-apps | grep -i WebDriverAgent
```

你需要选 **带 `.xctrunner` 后缀** 的那一行作为 `<WDA_XCTRUNNER_BUNDLE_ID>`。

3) 启动（Wi‑Fi 直连）：

```bash
bash scripts/run_wda_preinstalled_devicectl.sh start \
  --device <UDID> \
  --bundle-id <WDA_XCTRUNNER_BUNDLE_ID> \
  --wda-url http://<iphone-ip>:8100
```

其中 `<iphone-ip>` 可在 iPhone `设置 -> Wi‑Fi -> 当前网络` 里查看。

4) 验证：

```bash
python ios.py --wda-url http://<iphone-ip>:8100 --wda-status
```

需要停止时：

```bash
bash scripts/run_wda_preinstalled_devicectl.sh stop --device <UDID> --bundle-id <WDA_XCTRUNNER_BUNDLE_ID>
```

#### 2. 方案选择（覆盖所有方案，按推荐顺序）

如果你遇到下面这些情况，再从这里选其它方案：

- 你还没装过 `WebDriverAgentRunner-Runner` / 需要签名排障 → 用 Xcode `Product > Test` 跑通一次
- 你的局域网互访不稳定/受限 → 用 USB + `iproxy` 固定访问 `http://127.0.0.1:8100`
- 你仍想走 UI Test，但想更快重启 → `build-for-testing` + `test-without-building`
- 你希望工具链托管 XCTest 会话 → Appium（可选）

决策树：

- 优先 Wi‑Fi 直连（`http://<iphone-ip>:8100`）且希望日常不再跑 `xcodebuild ... test`
  - 前提：手机上已安装 `WebDriverAgentRunner-Runner`
  - 选：`devicectl --no-activate`（推荐）→ `docs/recipes/run_wda_preinstalled_devicectl.md`
- 首次安装/签名排障
  - 选：Xcode `Product > Test`（UI Test）
- 最稳兜底（不依赖局域网互访）
  - 选：USB + `iproxy` → `docs/recipes/iproxy_from_source.md`
- 更快重启（仍走 UI Test）
  - 选：`xcodebuild test-without-building` → `docs/recipes/run_wda_xcodebuild.md`
- 可选：工具链托管 session
  - 选：Appium “preinstalled WDA” → `docs/recipes/run_wda_preinstalled_appium.md`

速查表：

| 场景 | 启动 WDA | 访问 WDA | 入口 |
| --- | --- | --- | --- |
| **首选**：Wi‑Fi + 日常不再跑 `xcodebuild` | `devicectl --no-activate`（已安装 `WebDriverAgentRunner-Runner`） | `http://<iphone-ip>:8100` | `scripts/run_wda_preinstalled_devicectl.sh` |
| 首次安装/签名排障 | Xcode `Product > Test`（UI Test） | Wi‑Fi：`http://<iphone-ip>:8100` | 本节 “安装 Runner” |
| 最稳兜底（不依赖局域网互访） | Xcode / `devicectl` 均可 | `iproxy` → `http://127.0.0.1:8100` | `docs/recipes/iproxy_from_source.md` |
| 更快重启（仍走 UI Test） | `xcodebuild test-without-building` | 同上（Wi‑Fi 或 `iproxy`） | `scripts/run_wda_xcodebuild.sh` |
| 可选：工具链托管 session | Appium XCUITest（preinstalled WDA） | 同上（Wi‑Fi 或 `iproxy`） | `scripts/run_wda_preinstalled_appium.sh` |

补充：通过 Xcode UI Test 启动 WDA 时，`WebDriverAgentRunner-Runner` 可能会被重新安装/更新，从而把 iPhone 里该 App 的 `Wireless Data` 重置回 Off。日常用 `devicectl`（启动已安装 Runner）或使用 `iproxy` 都能显著减少/绕开这个问题。

### 3. 运行 iOS 版 Phone Agent

1) 确认 WDA 可访问：

```bash
python ios.py --wda-url http://<iphone-ip>:8100 --wda-status
```

2) 开始执行任务：

```bash
python ios.py --wda-url http://<iphone-ip>:8100 --base-url http://localhost:8000/v1 --model "autoglm-phone-9b" "打开 Safari 搜索 iPhone 使用技巧"
```

可选参数：

- `--insecure`：当 WDA 使用 https 且证书无法校验时使用
- `--scale-factor` / `PHONE_AGENT_IOS_SCALE_FACTOR`：若点击/滑动有偏移，可手动指定 1/2/3
- `--list-apps`：查看内置 App 名 -> bundleId 映射（位于 `phone_agent/ios/apps.py`）

说明：iOS 端只依赖 WebDriverAgent（WDA）可达，不需要安装 `libimobiledevice`。

## 部署准备工作

### 1. 安装依赖（Android / iOS 通用）

```bash
pip install -r requirements.txt 
pip install -e .
```

### 2. 连接设备（按平台）

#### Android：配置 ADB

确认 **USB 数据线具有数据传输功能**, 而不是仅有充电功能

确保已安装 ADB 并使用 **USB 数据线** 连接设备：

```bash
# 检查已连接的设备
adb devices

# 输出结果应显示你的设备，如：
# List of devices attached
# emulator-5554   device
```

#### iPhone（iOS）：确保 WDA 可达

iOS 不使用 ADB；只要你的 WDA（WebDriverAgent）可访问即可（见上方 “iPhone 环境准备”）。

你可以先用以下命令做一次连通性检查（`<WDA_URL>` 二选一）：

- Wi‑Fi 直连：`http://<iphone-ip>:8100`
- USB + `iproxy`：`http://127.0.0.1:8100`

```bash
python ios.py --wda-url <WDA_URL> --wda-status
```

### 3. 启动模型服务（Android / iOS 通用）

你可以选择自行部署模型服务，或使用第三方模型服务商。

#### 选项 A: 使用第三方模型服务

如果你不想自行部署模型，可以使用以下已部署我们模型的第三方服务：

**1. 智谱 BigModel**

- 文档: https://docs.bigmodel.cn/cn/api/introduction
- `--base-url`: `https://open.bigmodel.cn/api/paas/v4`
- `--model`: `autoglm-phone`
- `--apikey`: 在智谱平台申请你的 API Key

**2. ModelScope(魔搭社区)**

- 文档: https://modelscope.cn/models/ZhipuAI/AutoGLM-Phone-9B
- `--base-url`: `https://api-inference.modelscope.cn/v1`
- `--model`: `ZhipuAI/AutoGLM-Phone-9B`
- `--apikey`: 在 ModelScope 平台申请你的 API Key

使用第三方服务的示例：

```bash
# Android：使用智谱 BigModel
python main.py --base-url https://open.bigmodel.cn/api/paas/v4 --model "autoglm-phone" --apikey "your-bigmodel-api-key" "打开美团搜索附近的火锅店"

# iOS：使用智谱 BigModel（需要额外加 --wda-url）
python ios.py --wda-url <WDA_URL> --base-url https://open.bigmodel.cn/api/paas/v4 --model "autoglm-phone" --apikey "your-bigmodel-api-key" "打开 Safari 搜索附近的火锅店"

# Android：使用 ModelScope
python main.py --base-url https://api-inference.modelscope.cn/v1 --model "ZhipuAI/AutoGLM-Phone-9B" --apikey "your-modelscope-api-key" "打开美团搜索附近的火锅店"

# iOS：使用 ModelScope（需要额外加 --wda-url）
python ios.py --wda-url <WDA_URL> --base-url https://api-inference.modelscope.cn/v1 --model "ZhipuAI/AutoGLM-Phone-9B" --apikey "your-modelscope-api-key" "打开 Safari 搜索附近的火锅店"
```

#### 选项 B: 自行部署模型

如果你希望在本地或自己的服务器上部署模型：

1. 按照 `requirements.txt` 中 `For Model Deployment` 章节自行安装推理引擎框架。

对于 SGLang，除了使用 pip 安装，你也可以使用官方 docker：
>
> ```shell
> docker pull lmsysorg/sglang:v0.5.6.post1
> ```
>
> 进入容器，执行
>
> ```
> pip install nvidia-cudnn-cu12==9.16.0.29
> ```

对于 vLLM，除了使用 pip 安装，你也可以使用官方 docker：
>
> ```shell
> docker pull vllm/vllm-openai:v0.12.0
> ```
>
> 进入容器，执行
>
> ```
> pip install -U transformers --pre
> ```

**注意**：上述步骤出现的关于 transformers 的依赖冲突可以忽略。

1. 在对应容器或者实体机中（非容器安装）下载模型，通过 SGLang / vLLM 启动，得到 OpenAI 格式服务。这里提供一个 vLLM 部署方案，请严格遵循我们提供的启动参数：

- vLLM:

```shell
python3 -m vllm.entrypoints.openai.api_server \
 --served-model-name autoglm-phone-9b \
 --allowed-local-media-path /   \
 --mm-encoder-tp-mode data \
 --mm_processor_cache_type shm \
 --mm_processor_kwargs "{\"max_pixels\":5000000}" \
 --max-model-len 25480  \
 --chat-template-content-format string \
 --limit-mm-per-prompt "{\"image\":10}" \
 --model zai-org/AutoGLM-Phone-9B \
 --port 8000
```

- SGLang:

```shell
python3 -m sglang.launch_server --model-path  zai-org/AutoGLM-Phone-9B \
        --served-model-name autoglm-phone-9b  \
        --context-length 25480  \
        --mm-enable-dp-encoder   \
        --mm-process-config '{"image":{"max_pixels":5000000}}'  \
        --port 8000
```

- 该模型结构与 `GLM-4.1V-9B-Thinking` 相同，关于模型部署的详细内容，你也可以查看 [GLM-V](https://github.com/zai-org/GLM-V)
  获取模型部署和使用指南。

- 运行成功后，将可以通过 `http://localhost:8000/v1` 访问模型服务。如果您在远程服务器部署模型，使用该服务器的 IP 访问模型。

### 4. 检查模型部署

模型服务启动后，可以使用检查脚本验证部署是否成功：

```bash
python scripts/check_deployment_cn.py --base-url http://<ip>:<port>/v1 --model 模型名称
```

脚本将发送测试请求并展示模型的推理结果，你可以根据输出判断模型部署是否正常工作。

基于给定的任务，预期输出如下。**如果思维链长度很短，或者出现了乱码，很可能是模型部署失败**，请仔细检查文档要求的配置和依赖。

```
<think>用户想要比较这个洗发水在京东和淘宝上的价格，然后选择最便宜的平台下单。当前在小红书 app 上，显示的是一个关于 LUMMI MOOD 洗发水的帖子。

我需要：
1. 先启动京东 app，搜索这个洗发水
2. 查看京东的价格
3. 再启动淘宝 app，搜索这个洗发水
4. 查看淘宝的价格
5. 比较价格后，选择最便宜的京东或淘宝下单

首先，我需要从当前的小红书界面退出，然后启动京东 app。</think>
<answer>do(action="Launch", app="京东")</answer>
```

**参数说明：**
- `--base-url`: 模型服务地址(根据实际部署地址修改)
- `--model`: 模型名称
- `--messages-file`: 可选，指定自定义测试消息文件(默认使用 `scripts/sample_messages.json`)

## 使用 AutoGLM

### 命令行

根据你部署的模型, 设置 `--base-url` 和 `--model` 参数. 例如:

```bash
# 交互模式
python main.py --base-url http://localhost:8000/v1 --model "autoglm-phone-9b"

# 指定模型端点
python main.py --base-url http://localhost:8000/v1 "打开美团搜索附近的火锅店"

# 使用 API Key 进行认证
python main.py --apikey sk-xxxxx

# 使用英文 system prompt
python main.py --lang en --base-url http://localhost:8000/v1 "Open Chrome browser"

# 列出支持的应用
python main.py --list-apps
```

### Python API

```python
from phone_agent import PhoneAgent
from phone_agent.model import ModelConfig

# Configure model
model_config = ModelConfig(
    base_url="http://localhost:8000/v1",
    model_name="autoglm-phone-9b",
)

# 创建 Agent
agent = PhoneAgent(model_config=model_config)

# 执行任务
result = agent.run("打开淘宝搜索无线耳机")
print(result)
```

## 远程调试

Phone Agent 支持通过 WiFi/网络进行远程 ADB 调试，无需 USB 连接即可控制设备。

### 配置远程调试

#### 在手机端开启无线调试

确保手机和电脑在同一个 WiFi 中，如图所示

![开启无线调试](resources/setting.png)

#### 在电脑端使用标准 ADB 命令

```bash

# 通过 WiFi 连接, 改成手机显示的 IP 地址和端口
adb connect 192.168.1.100:5555

# 验证连接
adb devices
# 应显示：192.168.1.100:5555    device
```

### 设备管理命令

```bash
# 列出所有已连接设备
adb devices

# 连接远程设备
adb connect 192.168.1.100:5555

# 断开指定设备
adb disconnect 192.168.1.100:5555

# 指定设备执行任务
python main.py --device-id 192.168.1.100:5555 --base-url http://localhost:8000/v1 --model "autoglm-phone-9b" "打开抖音刷视频"
```

### Python API 远程连接

```python
from phone_agent.adb import ADBConnection, list_devices

# 创建连接管理器
conn = ADBConnection()

# 连接远程设备
success, message = conn.connect("192.168.1.100:5555")
print(f"连接状态: {message}")

# 列出已连接设备
devices = list_devices()
for device in devices:
    print(f"{device.device_id} - {device.connection_type.value}")

# 在 USB 设备上启用 TCP/IP
success, message = conn.enable_tcpip(5555)
ip = conn.get_device_ip()
print(f"设备 IP: {ip}")

# 断开连接
conn.disconnect("192.168.1.100:5555")
```

### 远程连接问题排查

**连接被拒绝：**

- 确保设备和电脑在同一网络
- 检查防火墙是否阻止 5555 端口
- 确认已启用 TCP/IP 模式：`adb tcpip 5555`

**连接断开：**

- WiFi 可能断开了，使用 `--connect` 重新连接
- 部分设备重启后会禁用 TCP/IP，需要通过 USB 重新启用

**多设备：**

- 使用 `--device-id` 指定要使用的设备
- 或使用 `--list-devices` 查看所有已连接设备

## 配置

### 自定义 SYSTEM PROMPT

系统提供中英文两套 prompt，通过 `--lang` 参数切换：

- `--lang cn` - 中文 prompt(默认)，配置文件：`phone_agent/config/prompts_zh.py`
- `--lang en` - 英文 prompt，配置文件：`phone_agent/config/prompts_en.py`

可以直接修改对应的配置文件来增强模型在特定领域的能力，或通过注入 app 名称禁用某些 app。

### 环境变量

| 变量                      | 描述               | 默认值                        |
|-------------------------|------------------|----------------------------|
| `PHONE_AGENT_BASE_URL`  | 模型 API 地址        | `http://localhost:8000/v1` |
| `PHONE_AGENT_MODEL`     | 模型名称             | `autoglm-phone-9b`         |
| `PHONE_AGENT_API_KEY`   | 模型认证 API Key     | `EMPTY`                    |
| `PHONE_AGENT_MAX_STEPS` | 每个任务最大步数         | `100`                      |
| `PHONE_AGENT_DEVICE_ID` | ADB 设备 ID        | (自动检测)                     |
| `PHONE_AGENT_LANG`      | 语言 (`cn` 或 `en`) | `cn`                       |

### 模型配置

```python
from phone_agent.model import ModelConfig

config = ModelConfig(
    base_url="http://localhost:8000/v1",
    api_key="EMPTY",  # API 密钥(如需要)
    model_name="autoglm-phone-9b",  # 模型名称
    max_tokens=3000,  # 最大输出 token 数
    temperature=0.1,  # 采样温度
    frequency_penalty=0.2,  # 频率惩罚
)
```

### Agent 配置

```python
from phone_agent.agent import AgentConfig

config = AgentConfig(
    max_steps=100,  # 每个任务最大步数
    device_id=None,  # ADB 设备 ID(None 为自动检测)
    lang="cn",  # 语言选择：cn(中文)或 en(英文)
    verbose=True,  # 打印调试信息(包括思考过程和执行动作)
)
```

### Verbose 模式输出

当 `verbose=True` 时，Agent 会在每一步输出详细信息：

```
==================================================
💭 思考过程:
--------------------------------------------------
当前在系统桌面，需要先启动小红书应用
--------------------------------------------------
🎯 执行动作:
{
  "_metadata": "do",
  "action": "Launch",
  "app": "小红书"
}
==================================================

... (执行动作后继续下一步)

==================================================
💭 思考过程:
--------------------------------------------------
小红书已打开，现在需要点击搜索框
--------------------------------------------------
🎯 执行动作:
{
  "_metadata": "do",
  "action": "Tap",
  "element": [500, 100]
}
==================================================

🎉 ================================================
✅ 任务完成: 已成功搜索美食攻略
==================================================
```

这样可以清楚地看到 AI 的推理过程和每一步的具体操作。

## 支持的应用

Phone Agent 支持 50+ 款主流中文应用：

| 分类   | 应用              |
|------|-----------------|
| 社交通讯 | 微信、QQ、微博        |
| 电商购物 | 淘宝、京东、拼多多       |
| 美食外卖 | 美团、饿了么、肯德基      |
| 出行旅游 | 携程、12306、滴滴出行   |
| 视频娱乐 | bilibili、抖音、爱奇艺 |
| 音乐音频 | 网易云音乐、QQ 音乐、喜马拉雅 |
| 生活服务 | 大众点评、高德地图、百度地图  |
| 内容社区 | 小红书、知乎、豆瓣       |

运行 `python main.py --list-apps` 查看完整列表。

## 可用操作

Agent 可以执行以下操作：

| 操作           | 描述              |
|--------------|-----------------|
| `Launch`     | 启动应用            |  
| `Tap`        | 点击指定坐标          |
| `Type`       | 输入文本            |
| `Swipe`      | 滑动屏幕            |
| `Back`       | 返回上一页           |
| `Home`       | 返回桌面            |
| `Long Press` | 长按              |
| `Double Tap` | 双击              |
| `Wait`       | 等待页面加载          |
| `Take_over`  | 请求人工接管(登录/验证码等) |

## 自定义回调

处理敏感操作确认和人工接管：

```python
def my_confirmation(message: str) -> bool:
    """敏感操作确认回调"""
    return input(f"确认执行 {message}？(y/n): ").lower() == "y"


def my_takeover(message: str) -> None:
    """人工接管回调"""
    print(f"请手动完成: {message}")
    input("完成后按回车继续...")


agent = PhoneAgent(
    confirmation_callback=my_confirmation,
    takeover_callback=my_takeover,
)
```

## 示例

查看 `examples/` 目录获取更多使用示例：

- `basic_usage.py` - 基础任务执行
- 单步调试模式
- 批量任务执行
- 自定义回调

## 二次开发

### 配置开发环境

二次开发需要使用开发依赖：

```bash
pip install -e ".[dev]"
```

### 运行测试

```bash
pytest tests/
```

### 完整项目结构

```
phone_agent/
├── __init__.py              # 包导出
├── agent.py                 # Android PhoneAgent
├── agent_base.py            # 通用 Agent 循环/基类
├── cli_checks.py            # CLI 环境自检
├── adb/                     # Android ADB 工具
│   ├── connection.py        # 远程/本地连接管理
│   ├── screenshot.py        # 屏幕截图
│   ├── input.py             # 文本输入 (ADB Keyboard)
│   └── device.py            # 设备控制 (点击、滑动等)
├── ios/                     # iOS 相关实现
│   ├── agent.py             # IOSPhoneAgent
│   ├── action_handler.py    # iOS 动作执行器
│   ├── apps.py              # App 名 -> bundleId 映射
│   └── wda/                 # WebDriverAgent (WDA) HTTP 封装
│       ├── wda_client.py    # WDA 客户端
│       ├── device.py        # 触控/系统动作
│       ├── input.py         # 文本输入
│       ├── screenshot.py    # 屏幕截图
│       └── connection.py    # 连接/健康检查
├── actions/                 # 动作处理
│   ├── base_handler.py      # 通用 handler 基类
│   ├── handler.py           # Android handler
│   ├── parsing.py           # 动作解析/清洗
│   └── types.py             # 动作类型
├── config/                  # 配置
│   ├── apps.py              # 支持的应用映射 (Android)
│   ├── i18n.py              # 文案与多语言
│   ├── prompts.py           # prompt 入口
│   ├── prompts_zh.py        # 中文系统提示词
│   ├── prompts_en.py        # 英文系统提示词
│   └── timing.py            # timing 配置
└── model/                   # AI 模型客户端
    └── client.py            # OpenAI 兼容客户端
```

## 常见问题

我们列举了一些常见的问题，以及对应的解决方案：

### 设备未找到

尝试通过重启 ADB 服务来解决：

```bash
adb kill-server
adb start-server
adb devices
```

如果仍然无法识别，请检查：

1. USB 调试是否已开启
2. 数据线是否支持数据传输(部分数据线仅支持充电)
3. 手机上弹出的授权框是否已点击「允许」
4. 尝试更换 USB 接口或数据线

### 能打开应用，但无法点击

部分机型需要同时开启两个调试选项才能正常使用：

- **USB 调试**
- **USB 调试(安全设置)**

请在 `设置 → 开发者选项` 中检查这两个选项是否都已启用。

### 文本输入不工作

1. 确保设备已安装 ADB Keyboard
2. 在设置 > 系统 > 语言和输入法 > 虚拟键盘 中启用
3. Agent 会在需要输入时自动切换到 ADB Keyboard

### 截图失败(黑屏)

这通常意味着应用正在显示敏感页面(支付、密码、银行类应用)。Agent 会自动检测并请求人工接管。

### windows 编码异常问题

报错信息形如 `UnicodeEncodeError gbk code`

解决办法: 在运行代码的命令前面加上环境变量: `PYTHONIOENCODING=utf-8`

### 交互模式非 TTY 环境无法使用

报错形如: `EOF when reading a line`

解决办法: 使用非交互模式直接指定任务, 或者切换到 TTY 模式的终端应用.

### 引用

如果你觉得我们的工作有帮助，请引用以下论文：

```bibtex
@article{liu2024autoglm,
  title={Autoglm: Autonomous foundation agents for guis},
  author={Liu, Xiao and Qin, Bo and Liang, Dongzhu and Dong, Guang and Lai, Hanyu and Zhang, Hanchen and Zhao, Hanlin and Iong, Iat Long and Sun, Jiadai and Wang, Jiaqi and others},
  journal={arXiv preprint arXiv:2411.00820},
  year={2024}
}
@article{xu2025mobilerl,
  title={MobileRL: Online Agentic Reinforcement Learning for Mobile GUI Agents},
  author={Xu, Yifan and Liu, Xiao and Liu, Xinghan and Fu, Jiaqi and Zhang, Hanchen and Jing, Bohao and Zhang, Shudan and Wang, Yuting and Zhao, Wenyi and Dong, Yuxiao},
  journal={arXiv preprint arXiv:2509.18119},
  year={2025}
}
```

---

## 自动化部署指南(面向 AI)

> **本章节专为 AI 助手(如 Claude Code)设计，用于自动化部署 Open-AutoGLM。**
>
> 如果你是人类读者，可以跳过本章节，按照上面的文档操作即可。

---

### 项目概述

Open-AutoGLM 是一个手机 Agent 框架：
- **输入**：用户的自然语言指令(如"打开微信发消息给张三")
- **输出**：自动操作用户的安卓手机完成任务
- **原理**：截图 → 视觉模型理解界面 → 输出点击坐标 → ADB 执行操作 → 循环

架构分为两部分：
1. **Agent 代码**(本仓库)：运行在用户电脑上，负责调用模型、解析动作、控制手机
2. **视觉模型服务**：可以是远程 API，也可以本地部署

---

### 部署前置检查

在开始部署前，请逐项向用户确认以下内容：

#### 硬件环境
- [ ] 用户有一台安卓手机(Android 7.0+)
- [ ] 用户有一根支持数据传输的 USB 数据线(不是仅充电线)
- [ ] 手机和电脑可以通过数据线连接

#### 手机端配置
- [ ] 手机已开启「开发者模式」(设置 → 关于手机 → 连续点击版本号 7 次)
- [ ] 手机已开启「USB 调试」(设置 → 开发者选项 → USB 调试)
- [ ] 部分机型需要同时开启「USB 调试(安全设置)」
- [ ] 手机已安装 ADB Keyboard 应用(下载地址：https://github.com/senzhk/ADBKeyBoard/blob/master/ADBKeyboard.apk)
- [ ] ADB Keyboard 已在系统设置中启用(设置 → 语言和输入法 → 启用 ADB Keyboard)

#### 模型服务确认(二选一)

**请明确询问用户：你是否已有可用的 AutoGLM 模型服务？**

- **选项 A：使用已部署的模型服务(推荐)**
  - 用户提供模型服务的 URL(如 `http://xxx.xxx.xxx.xxx:8000/v1`)
  - 无需本地 GPU，无需下载模型
  - 直接使用该 URL 作为 `--base-url` 参数

- **选项 B：本地部署模型(高配置要求)**
  - 需要 NVIDIA GPU(建议 24GB+ 显存)
  - 需要安装 vLLM 或 SGLang
  - 需要下载约 20GB 的模型文件
  - **如果用户是新手或不确定，强烈建议选择选项 A**

---

### 部署流程

#### 阶段一：环境准备

```bash
# 1. 安装 ADB 工具
# MacOS:
brew install android-platform-tools
# 或手动下载：https://developer.android.com/tools/releases/platform-tools

# Windows: 下载后解压，添加到 PATH 环境变量

# 2. 验证 ADB 安装
adb version
# 应输出版本信息

# 3. 连接手机并验证
# 用数据线连接手机，手机上点击「允许 USB 调试」
adb devices
# 应输出设备列表，如：
# List of devices attached
# XXXXXXXX    device
```

**如果 `adb devices` 显示空列表或 unauthorized：**
1. 检查手机上是否弹出授权框，点击「允许」
2. 检查 USB 调试是否开启
3. 尝试更换数据线或 USB 接口
4. 执行 `adb kill-server && adb start-server` 后重试

#### 阶段二：安装 Agent

```bash
# 1. 克隆仓库(如果还没有克隆)
git clone https://github.com/zai-org/Open-AutoGLM.git
cd Open-AutoGLM

# 2. 创建虚拟环境(推荐)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt
pip install -e .
```

**注意：不需要 clone 模型仓库，模型通过 API 调用。**

#### 阶段三：配置模型服务

**如果用户选择选项 A(使用已部署的模型)：**

你可以使用以下第三方模型服务：

1. **智谱 BigModel**
   - 文档：https://docs.bigmodel.cn/cn/api/introduction
   - `--base-url`：`https://open.bigmodel.cn/api/paas/v4`
   - `--model`：`autoglm-phone`
   - `--apikey`：在智谱平台申请你的 API Key

2. **ModelScope(魔搭社区)**
   - 文档：https://modelscope.cn/models/ZhipuAI/AutoGLM-Phone-9B
   - `--base-url`：`https://api-inference.modelscope.cn/v1`
   - `--model`：`ZhipuAI/AutoGLM-Phone-9B`
   - `--apikey`：在 ModelScope 平台申请你的 API Key

使用示例：

```bash
# 使用智谱 BigModel
python main.py --base-url https://open.bigmodel.cn/api/paas/v4 --model "autoglm-phone" --apikey "your-bigmodel-api-key" "打开美团搜索附近的火锅店"

# 使用 ModelScope
python main.py --base-url https://api-inference.modelscope.cn/v1 --model "ZhipuAI/AutoGLM-Phone-9B" --apikey "your-modelscope-api-key" "打开美团搜索附近的火锅店"
```

或者直接使用用户提供的其他模型服务 URL，跳过本地模型部署步骤。

**如果用户选择选项 B(本地部署模型)：**

```bash
# 1. 安装 vLLM
pip install vllm

# 2. 启动模型服务(会自动下载模型，约 20GB)
python3 -m vllm.entrypoints.openai.api_server \
  --served-model-name autoglm-phone-9b \
  --allowed-local-media-path / \
  --mm-encoder-tp-mode data \
  --mm_processor_cache_type shm \
  --mm_processor_kwargs "{\"max_pixels\":5000000}" \
  --max-model-len 25480 \
  --chat-template-content-format string \
  --limit-mm-per-prompt "{\"image\":10}" \
  --model zai-org/AutoGLM-Phone-9B \
  --port 8000

# 模型服务 URL 为：http://localhost:8000/v1
```

#### 阶段四：验证部署

```bash
# 在 Open-AutoGLM 目录下执行
# 将 {MODEL_URL} 替换为实际的模型服务地址

python main.py --base-url {MODEL_URL} --model "autoglm-phone-9b" "打开微信，对文件传输助手发送消息：部署成功"
```

**预期结果：**
- 手机自动打开微信
- 自动搜索「文件传输助手」
- 自动发送消息「部署成功」

---

### 异常处理

| 错误现象 | 可能原因 | 解决方案 |
|---------|---------|---------|
| `adb devices` 无输出 | USB 调试未开启或数据线问题 | 检查开发者选项，更换数据线 |
| `adb devices` 显示 unauthorized | 手机未授权 | 手机上点击「允许 USB 调试」|
| 能打开应用但无法点击 | 缺少安全调试权限 | 开启「USB 调试(安全设置)」|
| 中文输入变成乱码或无输入 | ADB Keyboard 未启用 | 在系统设置中启用 ADB Keyboard |
| 截图返回黑屏 | 敏感页面(支付/银行) | 正常现象，系统会自动处理 |
| 连接模型服务失败 | URL 错误或服务未启动 | 检查 URL，确认服务正在运行 |
| `ModuleNotFoundError` | 依赖未安装 | 执行 `pip install -r requirements.txt` |

---

### 部署要点

1. **优先确认手机连接**：在安装任何代码之前，先确保 `adb devices` 能看到设备
2. **不要跳过 ADB Keyboard**：没有它，中文输入会失败
3. **模型服务是外部依赖**：Agent 代码本身不包含模型，需要单独的模型服务
4. **遇到权限问题先检查手机设置**：大部分问题都是手机端配置不完整
5. **部署完成后用简单任务测试**：建议用「打开微信发消息给文件传输助手」作为验收标准

---

### 命令速查

```bash
# 检查 ADB 连接
adb devices

# 重启 ADB 服务
adb kill-server && adb start-server

# 安装依赖
pip install -r requirements.txt && pip install -e .

# 运行 Agent(交互模式)
python main.py --base-url {MODEL_URL} --model "autoglm-phone-9b"

# 运行 Agent(单次任务)
python main.py --base-url {MODEL_URL} --model "autoglm-phone-9b" "你的任务描述"

# 查看支持的应用列表
python main.py --list-apps
```

---

**部署完成的标志：手机能自动执行用户的自然语言指令。**
