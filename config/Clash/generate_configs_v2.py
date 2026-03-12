import os
import re
import datetime

# ================= 配置区域 =================
# 模板文件路径
# 支持环境变量：设置 GITHUB_ROOT 环境变量指向 GitHub 项目根目录
# 例如：GITHUB_ROOT=E:\Git\Github
GITHUB_ROOT = os.getenv('GITHUB_ROOT', '')
if GITHUB_ROOT:
    TEMPLATE_PATH = os.path.join(GITHUB_ROOT, "rule_config", "config", "Clash", "config_v2.yaml")
else:
    # 如果没有设置环境变量，使用脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    TEMPLATE_PATH = os.path.join(script_dir, "config_v2.yaml")

# 订阅地址列表文件路径
# 优先使用 subs.config (私密配置，不提交到 Git)
# 建议将 subs.config 放在工作目录外部，例如：
#   - Windows: E:\\Private\\subs.config
#   - Linux/Mac: ~/Private/subs.config
# 如果不存在，则使用 subs.config.example (示例模板，可提交到 Git)
URL_LIST_PATH = r"./subs.config"  # 修改为工作目录外的路径
URL_LIST_EXAMPLE_PATH = r"./subs.config.example"

# 自建节点文件路径
# 优先使用 custom_proxies.config (私密配置，不提交到 Git)
# 建议将 custom_proxies.config 放在工作目录外部，例如：
#   - Windows: E:\\Private\\custom_proxies.config
#   - Linux/Mac: ~/Private/custom_proxies.config
# 如果不存在，则使用 custom_proxies.config.example (示例模板，可提交到 Git)
CUSTOM_PROXIES_PATH = r"./custom_proxies.config"  # 修改为工作目录外的路径
CUSTOM_PROXIES_EXAMPLE_PATH = r"./custom_proxies.config.example"

# 输出文件夹路径 (默认在当前目录 output 文件夹，不存在会自动创建)
OUTPUT_DIR = r"./output/"

# ================= 辅助函数 =================

def load_custom_proxies():
    """
    加载自建节点配置
    返回：节点列表的 YAML 字符串，如果没有节点则返回 None
    """
    custom_file = None

    # 优先使用 custom_proxies.config (私密配置)
    if os.path.exists(CUSTOM_PROXIES_PATH):
        custom_file = CUSTOM_PROXIES_PATH
        print(f"✅ 找到自建节点配置: {CUSTOM_PROXIES_PATH}")
    elif os.path.exists(CUSTOM_PROXIES_EXAMPLE_PATH):
        custom_file = CUSTOM_PROXIES_EXAMPLE_PATH
        print(f"ℹ️ 使用示例自建节点配置: {CUSTOM_PROXIES_EXAMPLE_PATH}")

    if not custom_file:
        print(f"ℹ️ 未找到自建节点配置文件，跳过合并")
        return None

    try:
        with open(custom_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 跳过空文件或只有注释的文件
        lines = [line.strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]
        if not lines:
            print(f"ℹ️ 自建节点配置文件为空，跳过合并")
            return None

        # 检查是否有有效的节点配置（以 "- name:" 开头）
        has_proxies = any(line.startswith('- name:') or line.startswith('-name:') for line in lines)
        if not has_proxies:
            print(f"ℹ️ 自建节点配置文件中没有节点定义，跳过合并")
            return None

        print(f"✅ 成功加载自建节点配置")
        return content

    except Exception as e:
        print(f"⚠️ 读取自建节点配置失败: {e}")
        return None

def merge_custom_proxies(template_content, custom_proxies_yaml):
    """
    将自建节点合并到模板配置中
    """
    if not custom_proxies_yaml:
        return template_content

    # 查找 proxies: 部分的位置
    # 模板中的格式是：
    # proxies:
    # # 在此粘贴你的节点...

    # 使用正则找到 proxies: 后面的位置，插入自建节点
    pattern = r'(proxies:\s*\n)((?:#[^\n]*\n)*)'

    match = re.search(pattern, template_content)
    if match:
        # 在 proxies: 和注释之后插入自建节点
        insert_pos = match.end()

        # 确保自建节点内容格式正确（每行前面不需要额外缩进，因为已经是列表格式）
        merged_content = (
            template_content[:insert_pos] +
            custom_proxies_yaml +
            "\n" +
            template_content[insert_pos:]
        )

        print(f"✅ 已合并自建节点到配置文件")
        return merged_content
    else:
        print(f"⚠️ 警告：未找到 proxies: 部分，无法合并自建节点")
        return template_content

# ================= 主程序 =================

def generate_configs():
    # 1. 检查文件是否存在
    if not os.path.exists(TEMPLATE_PATH):
        print(f"❌ 错误：找不到模板文件: {TEMPLATE_PATH}")
        return

    # 优先使用 subs.config (私密配置)，如果不存在则使用 subs.config.example (示例模板)
    config_file = URL_LIST_PATH
    if not os.path.exists(URL_LIST_PATH):
        if os.path.exists(URL_LIST_EXAMPLE_PATH):
            config_file = URL_LIST_EXAMPLE_PATH
            print(f"ℹ️ 未找到 subs.config，使用示例配置: {URL_LIST_EXAMPLE_PATH}")
            print(f"💡 提示：请复制 subs.config.example 为 subs.config 并填入真实订阅地址")
        else:
            print(f"❌ 错误：找不到订阅文件: {URL_LIST_PATH} 或 {URL_LIST_EXAMPLE_PATH}")
            return
    else:
        print(f"✅ 使用私密配置: {URL_LIST_PATH}")

    # 2. 创建输出目录
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"📁 已创建输出目录: {OUTPUT_DIR}")

    # 3. 读取模板内容
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # 4. 加载自建节点配置
    custom_proxies = load_custom_proxies()

    # 5. 获取当前日期 (用于文件名)
    current_date = datetime.datetime.now().strftime("%Y%m%d")

    # 6. 读取订阅列表并处理
    print("🚀 开始处理订阅列表...")
    count = 0

    with open(config_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        # 跳过空行、注释行或格式错误的行
        if not line or line.startswith('#') or ':' not in line:
            continue

        # 分割名称和URL (只分割第一个冒号，防止URL中有冒号被切断)
        parts = line.split(':', 1)
        name = parts[0].strip()
        url = parts[1].strip()

        # 如果URL没有http开头，可能是分割问题，做简单的修正（视txt格式而定）
        if not url.startswith('http'):
            print(f"⚠️ 跳过格式可疑行: {line}")
            continue

        # 7. 执行替换操作
        # 正则说明：
        # 匹配 "订阅1": { ... url: "任意内容" ... }
        # 我们只替换 url: 后的双引号内的内容
        # 这里的正则假设模板中 订阅1 的格式是标准的 yaml 键值对

        # 为了更精准，我们直接查找 '订阅1' 所在的行，并替换该行中的 url
        # 这里的逻辑是：先复制模板内容 -> 查找 -> 替换 -> 保存

        new_content = template_content

        # 8. 合并自建节点（如果有）
        new_content = merge_custom_proxies(new_content, custom_proxies)

        # 9. 定义替换逻辑：查找 订阅1 及其后的 url: "..." 结构
        # 你的模板中是：订阅1: {type: http, url: "...", ...}
        # 我们用正则精准定位 "订阅1" 这一行里的 url 字段

        pattern = r'(订阅1\s*:\s*\{.*?url:\s*")([^"]+)(".*?\})'

        # 检查正则是否能匹配到
        if re.search(pattern, new_content):
            # \1 是 url: " 之前的内容
            # \3 是 " 之后的内容
            # 我们把中间的捕获组替换为新的 url
            new_content = re.sub(pattern, f'\\1{url}\\3', new_content, count=1)

            # 同时也建议把 path 也改一下，防止多个文件用同一个缓存路径导致冲突 (可选)
            # 比如把 path: ./providers/sub1.yaml 改为 path: ./providers/sub1_ykkCloud.yaml
            path_pattern = r'(订阅1\s*:\s*\{.*?path:\s*)([^\s,}]+)(.*?\})'
            new_path_name = f"./providers/sub_{name}.yaml"
            new_content = re.sub(path_pattern, f'\\1{new_path_name}\\3', new_content, count=1)

        else:
            print(f"⚠️ 警告：在模板中未找到 '订阅1' 的配置格式，跳过 {name}")
            continue

        # 10. 保存文件
        # 文件名格式：名称_日期.yaml
        filename = f"{name}_{current_date}.yaml"
        # 替换文件名中可能存在的非法字符 (如 / \ : * ? " < > |)
        filename = re.sub(r'[\\/*?:"<>|]', '_', filename)

        output_path = os.path.join(OUTPUT_DIR, filename)

        try:
            with open(output_path, 'w', encoding='utf-8') as out_f:
                out_f.write(new_content)
            print(f"✅ 已生成: {filename}")
            count += 1
        except Exception as e:
            print(f"❌ 保存失败 {filename}: {e}")

    print(f"\n🎉 处理完成！共生成 {count} 个配置文件。")
    print(f"📂 文件保存在: {OUTPUT_DIR}")

if __name__ == "__main__":
    generate_configs()
