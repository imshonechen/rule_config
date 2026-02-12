# 更新日志

## 2026-02-12 - 自建节点支持 + 文件命名优化

### 新增功能

1. **自建节点配置文件支持**
   - 新增 `custom_proxies.config.example` 示例文件
   - 支持在 `custom_proxies.config` 中配置自建节点
   - 脚本自动检测并合并自建节点到生成的配置文件

2. **自动合并逻辑**
   - 如果 `custom_proxies.config` 存在且包含有效节点配置，自动合并
   - 如果文件为空或只有注释，跳过合并
   - 自建节点插入到 `proxies:` 部分，与订阅节点一起使用

3. **文件命名统一优化**
   - 敏感数据文件统一使用 `.config` 后缀（`subs.config`、`custom_proxies.config`）
   - 示例模板文件统一使用 `.config.example` 后缀
   - 配置模板保持 `.yaml` 后缀，与敏感数据文件区分

4. **隐私保护**
   - `custom_proxies.config` 已添加到 `.gitignore`
   - 支持将配置文件放在工作目录外部（如 `E:\Private\`）

### 文件变更

- **新增**: `custom_proxies.config.example` - 自建节点配置示例
- **修改**: `generate_configs_v2.py` - 添加自建节点加载和合并功能
- **修改**: `.gitignore` - 排除 `custom_proxies.config`
- **修改**: `README.md` - 添加自建节点配置说明和文件命名说明

### 使用方法

1. 复制示例文件：
   ```bash
   cp custom_proxies.config.example custom_proxies.config
   ```

2. 编辑 `custom_proxies.config`，添加你的自建节点配置

3. 运行生成脚本：
   ```bash
   python generate_configs_v2.py
   ```

4. 脚本会自动将自建节点合并到每个生成的配置文件中

### 支持的节点类型

- VLESS
- Trojan
- VMess
- Shadowsocks
- Hysteria2
- 以及所有 mihomo/Clash 支持的协议类型

---

## 历史版本

### 初始版本
- 支持从订阅地址批量生成配置文件
- 支持环境变量 `GITHUB_ROOT`
- 节点名称重命名规则（YAML 锚点）
- 自动跳过注释行和空行
