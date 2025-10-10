# SteamDeck 서버 환경 정리

## OS / 환경
- SteamOS (Arch Linux 기반) + KDE Plasma + 커스텀 세팅

## 네트워크
- 공유기 SuperDMZ 적용 → 유선으로 공인 IP 직접 획득
- 외부/내부 접속 모두 원활 (RustDesk, Steam Remote, FVTT Web 확인 완료)

## 컨테이너 동작 상태 (podman, 일반 사용자 권한)
1. **RustDesk 서버 (hbbs)**
   - 컨테이너 ID: `05d80eb52749`
   - 포트: `21115-21116/tcp`, `21116/udp`, `21118/tcp`
   - 상태: 9일 전에 생성 → 현재 22시간째 가동
   - 이름: `rustdesk-hbbs`

2. **RustDesk 중계 서버 (hbbr)**
   - 컨테이너 ID: `5257f370dae1`
   - 포트: `21117/tcp`, `21119/tcp`
   - 상태: 6일 전에 생성 → 현재 22시간째 가동
   - 이름: `rustdesk-hbbr`

3. **Foundry VTT (Node.js 기반)**
   - 컨테이너 ID: `7ac6d669aebd`
   - 포트: `30000/tcp`
   - 상태: 4일 전에 생성 → 현재 22시간째 가동
   - 용도: FVTT 서버

## 리버스 프록시 (Caddy, root 권한)
- 설정 도메인: **`krdp.ddns.net`**
- 규칙:
  ```caddy
  krdp.ddns.net {
      reverse_proxy 127.0.0.1:30000
  }
  ```
- 목적: FVTT 서버 HTTPS 지원

- 향후 목표 : 분리관리
```caddyfile
yourdomain.com {
    # Foundry VTT (메인)
    handle / {
        reverse_proxy localhost:30000
    }
    
    # RustDesk API
    handle /rustdesk/api/* {
        uri strip_prefix /rustdesk/api
        reverse_proxy localhost:21114
    }
    
    # RustDesk ID
    handle /rustdesk/id/* {
        uri strip_prefix /rustdesk/id
        reverse_proxy localhost:21116
    }
    
    # RustDesk 릴레이
    handle /rustdesk/relay/* {
        uri strip_prefix /rustdesk/relay
        reverse_proxy localhost:21117
    }
}
```

## 방화벽 상태 (firewalld)
- 존: `public (default, active)`
- 허용 서비스: `dhcpv6-client`, `http`, `https`, `ssh`
- 허용 포트:
  - `1024-65535/tcp`
  - `1024-65535/udp`
  - `9/udp` (매직 패킷, WOL 용도로 추정)
- NAT/마스커레이드: `no` (직접 공인 IP라 불필요)

## 종합 정리
- 현재 스팀덱은 **공인 IP 직접 획득 + DMZ로 포트 전부 열림** 상태
- RustDesk 서버/중계, FVTT(Web, HTTPS 프록시), Steam Remote 모두 정상 가동 중
- 방화벽은 사실상 1024 이상 모든 포트 열려 있어서 외부 접근 제한은 거의 없음
- 내부/외부 접근 다 확인 완료 → 안정적인 “원격 제어 + TRPG 서버” 플랫폼으로 동작 중
