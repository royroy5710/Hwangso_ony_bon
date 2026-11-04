# -*- coding: utf-8 -*-
"""황소onY 시작 (자동 업데이트)
켤 때마다 GitHub 저장소에서 우리 관 프로그램 최신본을 받아서 실행해요.
- 인터넷이 안 되거나 열쇠(토큰)가 없어도 → 마지막으로 받은 프로그램으로 그대로 켜져요.
- 이 폴더의 '관.txt' 에 관 이름 (3관 · 본관), '토큰.txt' 에 읽기 전용 열쇠를 넣어 둬요.
- 파이썬 기본 부품만 씀 (따로 설치할 것 없음)."""
import hashlib
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

REPO = "royroy5710/hwangso-ony"
BRANCH = "main"
FILES = {                     # 관 → (저장소 안 경로, 이 컴퓨터에 둘 이름)
    "3관": ("3관/bogang.py", "bogang.py"),
    "본관": ("본관/bogang_bon.py", "bogang_bon.py"),
}
HERE = os.path.dirname(os.path.abspath(__file__))


def read_txt(name):
    try:
        with open(os.path.join(HERE, name), encoding="utf-8-sig") as f:
            return f.read().strip()
    except OSError:
        return ""


def blob_sha(data):
    """GitHub(git) 과 같은 방식의 파일 지문"""
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def api(path, token, raw=False, timeout=15):
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/contents/{urllib.request.quote(path)}?ref={BRANCH}",
        headers={"Authorization": f"Bearer {token}", "User-Agent": "hwangso-ony-updater",
                 "Accept": "application/vnd.github.raw" if raw else "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def update(branch_name, token):
    """최신본 받기 → (프로그램 경로, 안내 글)"""
    src, local = FILES[branch_name]
    target = os.path.join(HERE, local)
    if not token:
        return target, "열쇠(토큰.txt)가 없어서 업데이트를 건너뛰었어요."
    try:
        meta = json.loads(api(src, token))
        try:
            with open(target, "rb") as f:
                cur = f.read()
        except OSError:
            cur = None
        if cur is not None and blob_sha(cur) == meta.get("sha"):
            return target, "최신 버전이에요."
        data = api(src, token, raw=True, timeout=120)
        if blob_sha(data) != meta.get("sha"):
            return target, "받은 파일이 깨져 있어서 이전 버전으로 켜요."
        compile(data.decode("utf-8"), local, "exec")          # 문법이 깨진 파일이면 안 바꿈
        if cur is not None:
            with open(target + ".이전", "wb") as f:              # 바로 전 버전 (문제 생기면 되돌리기용)
                f.write(cur)
        tmp = target + ".받는중"
        with open(tmp, "wb") as f:
            f.write(data)
        os.replace(tmp, target)
        return target, "새 버전을 받았어요."
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            return target, "열쇠(토큰)가 맞지 않거나 기한이 지났어요 → 영은님께 알려주세요. 이전 버전으로 켜요."
        return target, f"업데이트 확인 실패 ({e.code}) → 이전 버전으로 켜요."
    except Exception as e:
        return target, f"업데이트 확인 실패 ({e.__class__.__name__}) → 이전 버전으로 켜요."


def main():
    br = read_txt("관.txt")
    if br not in FILES:
        print(f"[안내] 관.txt 에 관 이름을 적어주세요: {' · '.join(FILES)}  (지금: '{br}')")
        return 1
    target, msg = update(br, read_txt("토큰.txt"))
    print(f"[황소onY {br}] {msg}")
    if not os.path.exists(target):
        print("[안내] 프로그램 파일이 아직 없어요. 인터넷 · 토큰.txt 를 확인해주세요.")
        return 1
    return subprocess.call([sys.executable, target], cwd=HERE)


if __name__ == "__main__":
    sys.exit(main())
