# Network Config Diff Checker

ネットワーク機器の `running-config` を取得し、あらかじめ用意したゴールデンコンフィグ（基準設定ファイル）と差分を比較するツールです。  
Netmiko を利用して SSH 接続し、差分結果を色付きで出力します。

---

## 機能概要

- **Netmiko** を用いて機器にログインし、`show running-config` で現行設定を取得  
- リポジトリ内の **base_config.txt**（基準設定）と比較  
- 差分を **色付きでターミナルに表示**  
  - `+` 行は緑
  - `-` 行は赤
  - 差分のコンテキスト（`@@ ... @@`）は水色

---

## 必要なもの

1. **Python 3.7 以上**
2. **以下のPythonパッケージ**（pipでインストール）
   ```
   pip install netmiko PyYAML
   ```
3. ネットワーク機器への **SSH接続** 権限  
   - IPアドレス、ユーザー名、パスワード等を用意してください。

---

## ディレクトリ構成 (例)

```
.
├── check_config_diff.py
├── configs/
│   └── base_config.txt
├── devices.yaml.example
└── README.md
```

- `check_config_diff.py`: メインのスクリプト  
- `configs/base_config.txt`: 基準設定ファイル（比較元）  
- `devices.yaml.example`: 接続する機器情報のサンプルファイル（コピーして `devices.yaml` として利用）  

---

## デバイス情報ファイル (`devices.yaml.example`)

サンプルファイルを以下に示します。  
実際に使うときは `devices.yaml` にリネームして、各値を正しい情報に書き換えてください。

```yaml
devices:
  - name: "routerA"
    ip: "192.168.1.1"
    username: "admin"
    password: "password"
    device_type: "cisco_ios"
    base_config : "./config/routerA/config.txt"

  - name: "routerB"
    ip: "192.168.1.2"
    username: "admin"
    password: "password"
    device_type: "nec_ix"
    base_config : "./config/routerB/config.txt"
```

---

## 使い方

### 1. リポジトリのクローンまたはダウンロード

```
git clone https://github.com/naoya-is/diff-checker.git
cd diff-checker
```

### 2. Python環境 & 必要パッケージのインストール

```
pip install netmiko PyYAML
```

### 3. `devices.yaml` の準備

1. `devices.yaml.example` をコピーして `devices.yaml` として作成
2. 接続情報（IP、認証情報など）を正確に入力する

```
cp devices.yaml.example devices.yaml
vi devices.yaml    # or your favorite editor
```

### 4. `configs/base_config.txt` を事前に用意

```
mkdir -p configs
cp your_saved_config.txt configs/base_config.txt
```

### 5. スクリプトを実行

```
python check_config_diff.py
```

実行すると、YAMLに定義した各デバイスについて `show running-config` を取得し、  
`configs/base_config.txt` との差分をターミナルに表示します。

---

## 実行結果例

- **差分あり** の場合

```diff
=== 差分検出 ===
@@ -23,7 +23,7 @@
-interface GigabitEthernet0/1
- description Old Description
+ description New Description
```

- **差分なし** の場合

```
差分なし。設定は一致しています。
```

---

## よくある質問 (FAQ)

1. **他のベンダー機器で使えますか？**  
   はい。`device_type` を `cisco_ios` や `arista_eos`、`juniper_junos` などに変更すれば利用できます。  
   （[Netmiko公式ドキュメント](https://pypi.org/project/netmiko/)のサポートリストを参照）

2. **Windows で ANSI カラーコードが表示されません。**  
   - Windows Terminal または VSCode のターミナルを使用してください。  
   - 古い `cmd.exe` は対応していない場合があります。
