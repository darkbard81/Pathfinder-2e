# SteamDeck Overlay 정리 & HTTPS 인증서 발급 요약

## 1. Overlay ( `/var` ) 용량 정리
- 문제: `/var` 파티션(230MB)이 99% 사용 중 → `/var/lib/containers` 가 주범
- 원인: sudo를 통한 podman 및 flatpak 설치 uninstall해도 잔여파일이 남음
```bash
flatpak list --system
flatpak list --user
```
- 조치:
  ```bash
  # /var 사용량 확인
  sudo du -xh --max-depth=1 /var | sort -h

  # 컨테이너 데이터 확인
  sudo du -xh --max-depth=1 /var/lib | sort -h

  # 불필요한 Podman/Container 데이터 정리
  sudo podman system prune -a

  # 수동으로 컨테이너 저장소 제거
  sudo rm -rf /var/lib/containers/*
  ```

- 결과: `/var` 사용량 약 99% → 18% 로 감소, 정상 공간 확보

---

## 2. Caddy HTTPS 인증서 발급 & 적용
- 도메인: `krdp.ddns.net` (No-IP DDNS 사용)
- 포트포워딩: 공유기에서 80, 443 → SteamDeck IP로 전달
- 방화벽 열기:
  ```bash
  sudo firewall-cmd --zone=public --add-service=http --permanent
  sudo firewall-cmd --zone=public --add-service=https --permanent
  sudo firewall-cmd --reload
  ```

- `/etc/caddy/Caddyfile` 설정:
  ```caddyfile
  krdp.ddns.net {
      reverse_proxy 127.0.0.1:30000
  }
  ```

- Caddy 서비스 제어:
  ```bash
  # 설정 확인
  sudo caddy validate --config /etc/caddy/Caddyfile

  # 재시작
  sudo systemctl restart caddy

  # 상태 확인
  sudo systemctl status caddy
  ```

- 특징:
  - Let’s Encrypt 자동 인증서 발급 및 갱신 지원
  - 브라우저 → Caddy ↔ FoundryVTT 서버(30000) 통신이 HTTPS로 암호화됨
  - 재부팅 시 자동 실행됨 (`systemctl enable caddy` 덕분)

---

✅ 최종 결과  
- `/var` 공간 문제 해결  
- `https://krdp.ddns.net` 으로 외부에서도 안전하게 FoundryVTT 접속 가능
