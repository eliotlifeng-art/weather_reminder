# Google Colab 云端打包 APK 完整指南

---

## 一、准备工作

### 1. 注册 OpenWeatherMap API Key

1. 打开 https://openweathermap.org
2. 点 **Sign In** → **Create an Account**，注册并登录
3. 登录后点头像 → **My API Keys**，复制 Key（新 Key 等几分钟才生效）

### 2. 压缩项目文件

进入 `C:\Agent_proj\MiMo_proj\weather_reminder\`，选中以下文件右键压缩成 zip：

- `main.py`
- `buildozer.spec`
- `requirements.txt`
- `app/` 文件夹
- `ui/` 文件夹
- `assets/` 文件夹

**不要**压缩 `.venv` 和 `.github`。假设压缩后叫 `weather_reminder.zip`。

---

## 二、打开 Colab

1. 浏览器访问 https://colab.research.google.com
2. 登录 Google 账号
3. 点 **新建笔记本**

---

## 三、打包步骤（共 9 个单元格，按顺序跑）

---

### 单元格 1 — 加 4G 虚拟内存

```bash
!sudo fallocate -l 4G /swapfile
!sudo chmod 600 /swapfile
!sudo mkswap /swapfile
!sudo swapon /swapfile
!free -h
```

---

### 单元格 2 — 装系统依赖

```bash
!sudo apt-get update
!sudo apt-get install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

---

### 单元格 3 — 上传 zip

```python
from google.colab import files
import os
os.makedirs("weather_reminder", exist_ok=True)
%cd weather_reminder
print("⬆ 点「选择文件」，选 weather_reminder.zip")
uploaded = files.upload()
for fn in uploaded:
    if fn.endswith('.zip'):
        !unzip -o {fn}
        print("✅ 解压完成")
```

---

### 单元格 4 — 装 Python 依赖（锁定版本）

```bash
!pip install buildozer cython==0.29.37 kivy==2.2.1 kivymd==1.1.1 requests plyer
```

---

### 单元格 5 — 初始化 Buildozer（触发 SDK 下载）

```bash
!buildozer init || true
!buildozer android debug 2>&1 | head -30
```

等它开始跑，看到下载进度条后 **点 ■ 停止按钮中断它**。
这一步只是为了触发 Android SDK 下载，不需要跑完。

---

### 单元格 6 — 安装 AIDL 工具

```bash
!find /root/.buildozer -name "sdkmanager" -type f 2>/dev/null
```

看输出路径，如果路径是 `/root/.buildozer/android/platform/android-sdk/tools/bin/sdkmanager`，就跑：

```bash
!yes | /root/.buildozer/android/platform/android-sdk/tools/bin/sdkmanager --sdk_root=/root/.buildozer/android/platform/android-sdk "build-tools;37.0.0"
```

确认装好了：

```bash
!ls /root/.buildozer/android/platform/android-sdk/build-tools/
```

看到 `37.0.0` 文件夹就 OK。

---

### 单元格 7 — 后台打包

```bash
!rm -f build.log
!nohup bash -c 'export PATH=$PATH:/usr/local/bin && buildozer android debug' > build.log 2>&1 &
echo "打包已启动"
```

---

### 单元格 8 — 查进度（反复运行这个）

```bash
!tail -5 build.log
```

**成功标志**：
```
APK available at bin/weather_reminder-0.1.0-debug.apk
```

**失败标志**：看到 `Error` 或 `FAILED`，运行 `!tail -30 build.log` 把输出贴给我。

---

### 单元格 9 — 下载 APK

```python
from google.colab import files
import glob
apks = glob.glob("bin/*.apk")
if apks:
    print(f"✅ {apks[0]}")
    files.download(apks[0])
else:
    print("❌ 未找到APK")
```

---

## 四、装到手机

1. APK 文件传到手机（数据线 / 微信 / 网盘）
2. 手机文件管理器找到 APK，点击安装
3. 提示"未知来源"的话去设置里允许

## 五、使用 App

1. 打开 App → 点右上角齿轮 ⚙ 进设置
2. 粘贴 OpenWeatherMap API Key → 点 Save
3. 添加城市（英文名如 Shanghai）→ 点城市名设为默认
4. 设置提醒时间（默认 07:30）
5. 返回主页点刷新，看到天气就成功了

## 六、常见问题

| 问题 | 解决 |
|------|------|
| Colab 断开连接 | 重新打开，从步骤1重来 |
| 爆内存 | 确认步骤1的 swap 加了 |
| 手机装不上 | 需要 Android 5.0+ |
| App 闪退 | 检查 API Key 是否填对 |
