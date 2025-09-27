# 🎯 Steam Deck (Arch Linux) 현재 RustDesk 서버 상황 정리

>sudo steamos-readonly disable


1. 실행 환경
   - RustDesk 서버(hbbs, hbbr)를 **Podman 컨테이너 (root 권한)** 으로 실행 중
   - 컨테이너 상태 확인은 `sudo podman ps` 로 가능
   - 일반 `podman ps` 에는 안 보임 (rootless와 rootful Podman 분리 때문)

2. 컨테이너 상태
   - `rustdesk-hbbs` → rendezvous(시그널) 서버
     - 포트: TCP/UDP 21116, TCP 21115, 21118
   - `rustdesk-hbbr` → relay 서버
     - 포트: TCP 21117, 21119
   - 둘 다 `Up (정상 실행)` 상태

3. 네트워크/포트
   - `--network host` 옵션으로 실행 → 호스트와 동일 IP/포트 사용
   - 방화벽(firewalld)에 21115~21119 열림
   - 공유기 포트포워딩: 21115~21119 모두 192.168.219.193(Deck)으로 연결
   - DDNS 주소: `krdp.ddns.net` → 외부에서 접속 가능

4. Key & ID
   - Podman 컨테이너는 **삭제 후 run 하면 Key 새로 생성됨**
   - `start`/`stop` 으로 관리하면 Key 고정 유지됨
   - 현재 Key는 유지된 상태

5. 기타
   - 외부 접속 성공 확인 (회사 ↔ 집 Deck)
   - 내부망에서는 IP로도 접속 OK
   - DDNS 사용 시 loopback 문제 → 해결됨

# ✅ 관리 명령 예시
# 실행 중인 컨테이너 확인
sudo podman ps

# 로그 확인
sudo podman logs rustdesk-hbbs | tail -n 50
sudo podman logs rustdesk-hbbr | tail -n 50

# 중지 / 시작
sudo podman stop rustdesk-hbbs rustdesk-hbbr
sudo podman start rustdesk-hbbs rustdesk-hbbr

# 삭제 후 재생성(새 Key 생성됨)
sudo podman rm -f rustdesk-hbbs rustdesk-hbbr

# 원격 해상도 스케일링
