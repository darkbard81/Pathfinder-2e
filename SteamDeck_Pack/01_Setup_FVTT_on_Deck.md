# 🎯 Steam Deck (Arch Linux + KDE Plasma) FoundryVTT 실행 정리

## 1. 데이터 디렉터리 준비
```bash
mkdir -p ~/foundryvtt        # FoundryVTT Node 버전 압축 해제 경로
mkdir -p ~/foundry_data      # 월드/모듈/설정 데이터 저장소
unzip ~/Downloads/FoundryVTT-Node-13.348.zip -d ~/foundryvtt
```

## 2. Podman 컨테이너 실행 (개발 모드)
```bash
podman run -it --rm   --name fvtt-dev   -p 30000:30000   -v ~/foundryvtt:/app   -v ~/foundry_data:/data   node:20 bash
```

- `-p 30000:30000` : 외부 접속용 포트  
- `-v ~/foundryvtt:/app` : Foundry 소스코드 마운트  
- `-v ~/foundry_data:/data` : 영속 데이터 마운트  

## 3. 컨테이너 안에서 실행
```bash
cd /app
npm install
node main.mjs --dataPath=/data --port=30000
```

- `/data` : 월드, 모듈, 설정 저장  
- `--port=30000` : 브라우저 접속 포트  

## 4. 접속
- 로컬: `http://localhost:30000`  
- LAN: `http://<SteamDeck_IP>:30000`  
- 외부: `http://krdp.ddns.net:30000` (공유기 포트포워딩 필요)  

---

✅ 현재 상태:  
- FoundryVTT 13.348 (Node 버전) 정상 실행 중  
- Admin Password 및 PF2e 시스템 설치 완료  
- 새 월드 생성 + Gamemaster 계정 로그인까지 확인됨  
