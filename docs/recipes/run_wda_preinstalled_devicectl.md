# 用 devicectl 启动“已安装的 WDA”（不再跑 xcodebuild test）

## 背景

WebDriverAgent（WDA）通常通过 `xcodebuild ... test` 启动。这个方式在某些设备/系统上会导致 **Runner 被频繁安装/更新**，从而把 iPhone 的：

`Settings -> Apps -> WebDriverAgentRunner-Runner -> Wireless Data`

重置回 **Off**，进而导致 `http://<iphone-ip>:8100/status` 访问超时。

如果你希望 WDA **只安装一次**，后续只做“启动/停止”而不再跑 `xcodebuild test`，可以用 Xcode 自带的 `devicectl` 来启动已安装的 `*.xctrunner`。

---

## 关键点：必须加 `--no-activate`

直接执行（默认会 activate）：

```bash
xcrun devicectl device process launch --device <UDID> com.xxx.wda.xctrunner
```

常见会失败并退出，例如：

- `Failed to initialize for UI testing ... Failed to background test runner within 30.0s.`
- 或 `Exiting due to IDE disconnection.`

实践上需要加 `--no-activate` 才更稳定：

```bash
xcrun devicectl device process launch --device <UDID> --no-activate com.xxx.wda.xctrunner
```

---

## 最小步骤（推荐）

### 0) 前提

- 你已经至少成功用 Xcode 跑通一次 WDA（确保签名/信任流程 OK）。
- 手机上能看到 `WebDriverAgentRunner-Runner` 已安装（bundle id 类似 `com.xxx.wda.xctrunner`）。
- 你知道设备 UDID（Xcode 或 `xcrun devicectl list devices`）。

#### 可选：安装/更新一次 Runner（更可控）

如果你希望把“安装”单独做一次（后续只启动/停止），可以：

1) 找到 `WebDriverAgentRunner-Runner.app`（通常在 Xcode DerivedData 里）：

```bash
ls ~/Library/Developer/Xcode/DerivedData/WebDriverAgent-*/Build/Products/Debug-iphoneos/WebDriverAgentRunner-Runner.app
```

2) （可选）如果你在 iOS 17+ / 18 上遇到 `devicectl process launch` 立刻退出等问题，可以尝试把 Runner 包里的 `Frameworks/XC*.framework` 删除并重新签名：

```bash
bash scripts/prepare_wda_runner_for_devicectl.sh \
  --app ~/Library/Developer/Xcode/DerivedData/WebDriverAgent-*/Build/Products/Debug-iphoneos/WebDriverAgentRunner-Runner.app \
  --out /tmp/WDA-Prepared
```

3) 安装到设备（只需做一次，后续不再安装）：

```bash
xcrun devicectl device install app --device <UDID> /tmp/WDA-Prepared/WebDriverAgentRunner-Runner.app
```

4) 在 iPhone 上把 Wireless Data 打开一次（避免 LAN 访问超时）：

`Settings -> Apps -> WebDriverAgentRunner-Runner -> Wireless Data` → 选 **WLAN** 或 **WLAN & Cellular Data**

#### 如何获取 `*.xctrunner` 的 bundle id

在 mac 上执行（会列出设备上的开发者 App）：

```bash
xcrun devicectl device info apps --device <UDID> --include-all-apps | grep -i WebDriverAgent
```

输出里 `Bundle Identifier` 一列就是需要的 `*.xctrunner`（例如 `com.xxx.wda.xctrunner`）。

### 1) 启动 WDA（不再跑 xcodebuild）

```bash
UDID="<你的UDID>"
WDA_XCTRUNNER_BUNDLE_ID="<你的 WDA .xctrunner bundle id>"

xcrun devicectl device process launch --device "$UDID" --no-activate "$WDA_XCTRUNNER_BUNDLE_ID"
```

然后检查（Wi‑Fi 可达时）：

```bash
curl http://<iphone-ip>:8100/status
```

或者如果你走 USB + `iproxy`：

```bash
curl http://127.0.0.1:8100/status
```

### 2) 停止 WDA

你可以用仓库脚本自动找 pid 并终止：

```bash
bash scripts/run_wda_preinstalled_devicectl.sh stop --device "$UDID" --bundle-id "$WDA_XCTRUNNER_BUNDLE_ID"
```

---

## 一键脚本

仓库提供脚本把“启动/停止/等待可用”串起来：

```bash
bash scripts/run_wda_preinstalled_devicectl.sh start \
  --device <UDID> \
  --bundle-id <WDA_XCTRUNNER_BUNDLE_ID> \
  --wda-url http://<iphone-ip>:8100
```

如果你用 `iproxy`，把 `--wda-url` 改成 `http://127.0.0.1:8100`。你也可以用 `--port` 改端口（默认 8100）。
