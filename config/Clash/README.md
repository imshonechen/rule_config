# Mihomo/Clash 配置生成工具

这个工具用于根据模板文件和订阅地址列表，批量生成 mihomo 配置文件。

## 文件说明

- `config_v2.yaml` - mihomo 配置模板文件
- `config_shone.yaml` - 另一个配置模板（个人使用）
- `generate_configs_v2.py` - 配置生成脚本
- `subs.config.example` - 订阅地址配置示例（可提交到 Git）
- `custom_proxies.config.example` - 自建节点配置示例（可提交到 Git）
- `output/` - 生成的配置文件输出目录

## 使用方法

### 0. 配置环境变量（推荐）

为了让脚本能够正确找到模板文件，建议设置环境变量：

**Windows:**
```cmd
# 临时设置（仅当前命令行窗口有效）
set GITHUB_ROOT=E:\Git\Github

# 永久设置（推荐）
# 方法1：通过命令行
setx GITHUB_ROOT "E:\Git\Github"

# 方法2：通过系统设置
# 1. 右键"此电脑" -> "属性" -> "高级系统设置"
# 2. 点击"环境变量"
# 3. 在"用户变量"中点击"新建"
# 4. 变量名：GITHUB_ROOT
# 5. 变量值：E:\Git\Github
```

**Linux/Mac:**
```bash
# 临时设置（仅当前终端有效）
export GITHUB_ROOT=~/Git/Github

# 永久设置（推荐）
# 添加到 ~/.bashrc 或 ~/.zshrc
echo 'export GITHUB_ROOT=~/Git/Github' >> ~/.bashrc
source ~/.bashrc
```

**说明：**
- `GITHUB_ROOT` 指向你的 GitHub 项目根目录（如 `E:\Git\Github`）
- 脚本会自动拼接后续路径：`rule_config/config/Clash/config_v2.yaml`
- 如果不设置环境变量，脚本会自动使用脚本所在目录作为根目录
- 设置环境变量后，可以在任意位置运行脚本，也方便其他项目复用

### 1. 准备订阅配置文件

**推荐方式：将私密配置放在工作目录外部**

在工作目录外创建私密配置文件，例如：
- Windows: `E:\Private\subs.config`
- Linux/Mac: `~/Private/subs.config`

```bash
# Windows
mkdir E:\Private
copy subs.config.example E:\Private\subs.config
notepad E:\Private\subs.config

# Linux/Mac
mkdir -p ~/Private
cp subs.config.example ~/Private/subs.config
nano ~/Private/subs.config
```

然后编辑配置文件，填入你的真实订阅地址：

```
# 每行格式：NAME: URL
机场A: https://example.com/subscribe?token=your_token_here
机场B: https://another.com/sub?token=another_token
```

**修改脚本配置**：编辑 `generate_configs_v2.py` 第 14 行，将 `URL_LIST_PATH` 改为你的私密配置路径。

---

**备选方式：在工作目录内创建（不推荐）**

如果你想在工作目录内创建 `subs.config`：

```bash
cp subs.config.example subs.config
# 编辑 generate_configs_v2.py 第 14 行，改为：
# URL_LIST_PATH = r"./subs.config"
```

注意：虽然 `.gitignore` 会排除此文件，但它仍在工作目录中可被访问。

### 2. 配置自建节点（可选）

如果你有自建节点，可以创建 `custom_proxies.config` 文件：

**推荐方式：在工作目录外创建**

```bash
# Windows
copy custom_proxies.config.example E:\Private\custom_proxies.config
notepad E:\Private\custom_proxies.config

# Linux/Mac
cp custom_proxies.config.example ~/Private/custom_proxies.config
nano ~/Private/custom_proxies.config
```

然后编辑文件，添加你的自建节点：

```yaml
- name: 自建香港VLESS
  type: vless
  server: hk.example.com
  port: 443
  uuid: your-uuid-here
  network: ws
  tls: true
  udp: true
  ws-opts:
    path: /path
    headers:
      Host: hk.example.com

- name: 自建日本Trojan
  type: trojan
  server: jp.example.com
  port: 443
  password: your-password-here
  udp: true
  sni: jp.example.com
```

**修改脚本配置**：如果使用工作目录外的路径，需要修改 `generate_configs_v2.py` 中的 `CUSTOM_PROXIES_PATH`。

**备选方式：在工作目录内创建**

```bash
cp custom_proxies.config.example custom_proxies.config
# 编辑文件添加节点配置
```

注意：
- 如果 `custom_proxies.config` 文件存在且包含节点配置，脚本会自动合并到生成的配置文件中
- 如果文件为空或只有注释，脚本会跳过合并
- `custom_proxies.config` 已添加到 `.gitignore`，不会提交到 Git

### 3. 运行生成脚本

```bash
python generate_configs_v2.py
```

脚本会：
- 优先读取 `subs.config`（私密配置）
- 如果 `subs.config` 不存在，则读取 `subs.config.example`（示例配置）
- 检查并加载 `custom_proxies.config`（自建节点配置）
- 为每个订阅地址生成一个独立的配置文件
- 如果有自建节点，自动合并到每个生成的配置文件中
- 输出到 `output/` 目录，文件名格式：`名称_日期.yaml`

### 4. 使用生成的配置

生成的配置文件位于 `output/` 目录，可以直接导入到 mihomo/Clash 客户端使用。

## 配置文件格式

`subs.config` 文件格式：

```
# 每行格式：NAME: URL
# NAME 是订阅的名称（用于生成文件名）
# URL 是订阅地址（必须以 http:// 或 https:// 开头）

机场名称: https://订阅地址
```

支持的 URL 格式示例：
- `https://example.com/config/token123`
- `https://example.com/subscribe?token=token123`
- `https://example.com/sub?token123`
- `https://example.com/link/token123?clash=3&extend=1`

## 注意事项

1. **隐私保护**：
   - `subs.config` 包含私密订阅链接，已添加到 `.gitignore`，不会提交到 Git
   - `custom_proxies.config` 包含私密节点信息，已添加到 `.gitignore`，不会提交到 Git
2. **示例文件**：
   - `subs.config.example` 是公开的订阅配置示例模板，可以安全提交到 Git
   - `custom_proxies.config.example` 是公开的自建节点配置示例模板，可以安全提交到 Git
3. **输出目录**：`output/` 目录也在 `.gitignore` 中，生成的配置文件不会提交到 Git
4. **自建节点合并**：
   - 脚本会自动检测 `custom_proxies.config` 文件
   - 如果文件存在且包含有效节点配置（以 `- name:` 开头），会自动合并到生成的配置中
   - 如果文件为空或只有注释，会跳过合并
   - 自建节点会插入到 `proxies:` 部分，与订阅节点一起使用

## 配置模板说明

`config_v2.yaml` 模板包含以下特性：

- **节点重命名规则**：使用 YAML 锚点统一管理，自动标准化节点名称
  - 移除 Emoji 表情
  - 统一地区命名（香港、台湾、日本、新加坡、美国等）
  - 统一倍率格式（1x、2x 等）

- **代理组配置**：
  - 按地区分组（香港、台湾、日本、新加坡、美国）
  - 自动测速和故障转移
  - 高倍率节点单独分组

- **分流规则**：
  - Emby、PT、GitHub、AI 服务等专用分流
  - 流媒体服务分流（Netflix、YouTube、Disney+ 等）
  - 游戏平台分流（Steam、Epic 等）
  - 国内外站点智能分流

## 故障排除

### 找不到订阅文件

如果看到错误：`❌ 错误：找不到订阅文件`

解决方法：
1. 确保已创建 `subs.config` 文件
2. 或者至少保留 `subs.config.example` 文件

### URL 格式错误

如果看到警告：`⚠️ 跳过格式可疑行`

检查：
1. URL 是否以 `http://` 或 `https://` 开头
2. 每行格式是否为 `名称: URL`（注意冒号后有空格）
3. 是否有空行或注释行（以 `#` 开头的行会被跳过）

## 许可证

本项目配置文件和脚本仅供个人学习使用。
