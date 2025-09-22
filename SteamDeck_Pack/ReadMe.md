# 🔹 RustDesk 서버 Podman 설치/실행 정리

# 1. 컨테이너 실행 (Podman, host 네트워크 모드)
sudo podman run -d --name rustdesk-hbbs \
  --network host \
  docker.io/rustdesk/rustdesk-server hbbs

sudo podman run -d --name rustdesk-hbbr \
  --network host \
  docker.io/rustdesk/rustdesk-server hbbr


# 2. 컨테이너 관리 명령
sudo podman ps                      # 실행 중인 컨테이너 확인
sudo podman logs rustdesk-hbbs       # hbbs 로그 확인
sudo podman logs rustdesk-hbbr       # hbbr 로그 확인
sudo podman stop rustdesk-hbbs rustdesk-hbbr
sudo podman start rustdesk-hbbs rustdesk-hbbr
sudo podman rm -f rustdesk-hbbs rustdesk-hbbr


# 3. 포트 정보 (firewalld/포트포워딩 필요)
21115/tcp  # NAT 테스트용
21116/tcp  # Signal 서버
21116/udp  # Signal 서버 (UDP hole punching)
21117/tcp  # Relay 서버
21118/tcp  # Websocket
21119/tcp  # Relay Websocket


# 4. NAT Loopback 문제 해결 (내부망 접근 시)
# 내부 PC의 /etc/hosts 수정
sudo nano /etc/hosts
192.168.219.193   krdp.ddns.net

# 확인
ping krdp.ddns.net   # 내부에서는 192.168.219.193 으로 나와야 함
# 외부에서는 125.177.x.x (공인IP)로 정상 노출됨

# 5. 확인된 사실
- RustDesk 서버(hbbs/hbbr)는 정상적으로 Podman 컨테이너에서 실행 중
- 내부망에서는 로컬 IP 또는 hosts 수정으로 접속 가능
- 외부망에서는 DDNS + 포트포워딩으로 접속 성공
- 문제의 원인은 공유기의 NAT Loopback 미지원 → hosts 수정으로 해결

# ⬇️ 앞으로 다룰 주제
1. 재부팅 시 Podman 컨테이너 자동 실행 (systemd 등록)
2. RustDesk 성능 체크 (대역폭, 지연, 리소스 사용)
3. 다른 웹서비스(Podman/Docker 기반) 등록 및 병행 운영 방법

>sudo podman run -d \
  --name foundryvtt \
  -p 30000:30000 \
  -v /home/deck/foundrydata:/data \
  felddy/foundryvtt:latest
>
>krdp_client
krdp.ddns.net
noip.com
darkbard81jp@gmail.com
qz799b6
nA78zGn6Pezm
42E06P$B36
port : 3389
krdp_client
krdp160915
sudo tcpdump -i wlan0 icmp
125.177.78.44
