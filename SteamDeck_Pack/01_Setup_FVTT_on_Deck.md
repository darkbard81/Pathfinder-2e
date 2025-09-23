# 🚢 Foundry VTT 운영 전략 (Podman 선택)

## 1. 개발 vs 운영
- **개발·테스트** → Node.js 직행이 편리 (저장→F5 즉시 반영).
- **운영·서비스** → Podman 컨테이너가 안전하고 일관성 있음.
- 결론: **운영은 Podman으로**.

---

## 2. Podman으로 돌리는 구조
- 컨테이너 안에서 Foundry VTT(Node.js) 실행.
- 호스트 ↔ 컨테이너 연결은 **포트**랑 **볼륨**만 지정.
  ```bash
  podman run -d     --name foundry     -p 30000:30000     -v ~/foundry_data:/data     docker.io/felddy/foundryvtt:latest
  ```
- `/data` 볼륨에 월드, 모듈, 설정이 저장 → 백업/복구/이전이 쉬움.

---

## 3. 안전성
- **Node.js 직접 실행**: 모듈 코드가 호스트 권한을 그대로 사용 → 위험 노출 큼.
- **Podman 실행**: 마운트한 `/data` 외에는 컨테이너 샌드박스에 갇힘 → 호스트 보호.
- 특히 **외부 모듈** 같이 쓸 때 Podman이 훨씬 안심됨.

---

## 4. 서비스 관리
- 컨테이너니까 관리 명령어도 단순:
  - 시작: `podman start foundry`
  - 중지: `podman stop foundry`
  - 재시작: `podman restart foundry`
  - 로그: `podman logs -f foundry`
- 필요 없으면 `podman rm foundry`로 지우고 새 이미지 받으면 끝.

---

## 5. 네트워크
- 로컬 접속: `http://localhost:30000`
- 같은 LAN 기기 접속: `http://<SteamDeck_IP>:30000`
- 외부 접속: 공유기 포트포워딩 + 방화벽 개방 필요.
- 안전하게 운영하려면 리버스 프록시(Nginx/Caddy) + HTTPS 추천.

---

✅ **정리**
- **Podman = 서비스용 안정 선택**
- **Node.js = 개발용 빠른 루프**
- 외부 모듈이 얽히는 실서비스라면 Podman 쪽이 맞다.
