import subprocess
import sys
import tempfile
from pathlib import Path

dist_dir = Path(__file__).parent.parent.resolve()
print(f"Testing isolated install from: {dist_dir}")

with tempfile.TemporaryDirectory() as tmp:
    tpath = Path(tmp) / "demo_project"
    cmd_init = [
        sys.executable,
        str(dist_dir / "bootstrap.py"),
        "init",
        "--target",
        str(tpath),
        "--name",
        "StandaloneDemo",
        "--env",
        "democonda",
    ]
    res_init = subprocess.run(cmd_init, capture_output=True, text=True)
    print(res_init.stdout)
    if res_init.returncode != 0:
        print("Init stderr:", res_init.stderr)
        sys.exit(1)

    # Doctor check
    cmd_doc = [
        sys.executable,
        str(dist_dir / "bootstrap.py"),
        "doctor",
        "--target",
        str(tpath),
    ]
    res_doc = subprocess.run(cmd_doc, capture_output=True, text=True)
    print(res_doc.stdout)
    if "11/11" not in res_doc.stdout:
        print("Doctor failed!")
        sys.exit(1)

    # Verify rules deployed
    rule_file = tpath / ".agents" / "rules" / "context-health.md"
    assert rule_file.exists(), f"Rule file {rule_file} was not deployed!"

print("SUCCESS: Standalone package verified working in 100% isolation.")
