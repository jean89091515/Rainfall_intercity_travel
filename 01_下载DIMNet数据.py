"""从 Figshare 下载 DIMNet-CPC：合并 Parquet（432 MB）、Unit_Lookup、元数据与 README。

已存在且大小一致的文件会跳过。用 curl 下载，绕开本机 Python 的 SSL 证书问题。
"""
import json
import subprocess

from config import DIMNET_DIR, DIMNET_FILES

DIMNET_DIR.mkdir(parents=True, exist_ok=True)

meta = json.loads(subprocess.run(
    ["curl", "-sL", "https://api.figshare.com/v2/articles/33154163"],
    capture_output=True, text=True, check=True).stdout)
sizes = {f["name"]: f["size"] for f in meta["files"]}

for name, url in DIMNET_FILES.items():
    out = DIMNET_DIR / name
    if out.exists() and out.stat().st_size == sizes.get(name):
        print(f"跳过（已存在）: {name}")
        continue
    print(f"下载 {name}（{sizes.get(name, 0) / 1e6:.1f} MB）...")
    subprocess.run(["curl", "-L", "--fail", "-o", str(out), url], check=True)
    assert out.stat().st_size == sizes[name], f"{name} 大小不符，请重下"
print("完成:", DIMNET_DIR)
