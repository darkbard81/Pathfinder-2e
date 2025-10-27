# 🏠 Home Server & Network Setup

## 📡 네트워크 환경
- **인터넷 상품**: 500M 광랜 (최대 500Mbps)
- **실측 속도**: 평균 Download/Upload 약 350Mbps
- **장비 링크 속도**: 1Gbps (NIC ↔ 공유기)

## 🌐 게이트웨이 / 네트워크
- 게이트웨이 IP: `192.168.219.1`
- 내부 서버 IP: `192.168.219.193`
- DDNS 도메인: `fvtt.krpd.ddns.net`

## 🖥️ 서버 장비
- **호스트 장치**: SteamDeck (Arch Linux / SteamOS, X11 세션)
- **컨테이너 런타임**: Podman (`--net host` 모드 사용)
- **주요 서비스**:
  - **FVTT (Foundry VTT)**  
    - 포트: `30000` (Podman 컨테이너)
    - Caddy Reverse Proxy → HTTPS 제공
    - 외부 접근: `https://fvtt.krpd.ddns.net`
    - 내부 접근: `https://localhost` (Caddy 처리)

  - **RustDesk (원격 접속)**  
    - 릴레이 서버(hbbr/hbbs): Podman 컨테이너로 운영
    - 네트워크 모드: `--net host`

## 🔐 보안 / 인증
- Caddy를 이용한 HTTPS Reverse Proxy
- DDNS + 와일드카드 인증서 적용
- 내부 접속 시에도 HTTPS 지원

## 👥 사용자 규모
- 최대 동시 접속 인원: 약 4명
- 활용 목적: 소규모 TRPG 캠페인(FVTT 기반) 운영

## 📊 특징
- 소규모 서버 환경으로 AWS 등 외부 클라우드 서비스 불필요
- 가정용 환경에서도 충분한 대역폭과 안정성 확보
- 관리 포인트 최소화 (Podman 컨테이너 + Caddy 자동화)
