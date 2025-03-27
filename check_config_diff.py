import getpass
import yaml
import difflib
import os
from netmiko import ConnectHandler

# ANSI色定義
RED = '\033[91m'
GREEN = '\033[92m'
CYAN = '\033[96m'
RESET = '\033[0m'

# YAML読み込み
with open("devices.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

for dev in config["devices"]:
    print(f"\n=== デバイス: {dev['name']} ({dev['ip']}) の設定を比較中 ===")

    # 接続情報をNetmiko用に整形
    remote_device = {
        "ip": dev["ip"],
        "username": dev["username"],
        "password": dev["password"],
        "device_type": dev["device_type"],
        "global_delay_factor": 3,
        "fast_cli": False,
    }

    # もし password が None または空文字なら、対話式で入力を促す
    if not remote_device.get('password'):
        remote_device['password'] = getpass.getpass(prompt="Password: ")

    # 接続・設定取得
    conn = ConnectHandler(**remote_device)
    conn.enable()
    running_config = conn.send_command("show running-config")
    conn.disconnect()

    # Golden Configの読み込み
    base_path = dev["base_config"]
    if not os.path.exists(base_path):
        print(f"{RED}[ERROR] Golden config not found: {base_path}{RESET}")
        continue

    with open(base_path, "r", encoding="utf-8") as f:
        base_config = f.read()

    # 差分比較
    diff = list(difflib.unified_diff(
        base_config.splitlines(),
        running_config.splitlines(),
        fromfile=base_path,
        tofile=f"{dev['name']}_running_config",
        lineterm=""
    ))

    # 結果表示
    if diff:
        print(f"{CYAN}--- 差分あり ---{RESET}")
        for line in diff:
            if line.startswith('+') and not line.startswith('+++'):
                print(f"{GREEN}{line}{RESET}")
            elif line.startswith('-') and not line.startswith('---'):
                print(f"{RED}{line}{RESET}")
            elif line.startswith('@@'):
                print(f"{CYAN}{line}{RESET}")
            else:
                print(line)
    else:
        print(f"{GREEN}設定に差分はありません{RESET}")
