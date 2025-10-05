{ pkgs, ... }: {
  channel = "stable-24.11";

  packages = [
    pkgs.docker
    pkgs.cloudflared
    pkgs.socat
    pkgs.coreutils
    pkgs.gnugrep
  ];

  services.docker.enable = true;

  idx.workspace.onStart = {
    chromium = ''
      set -euo pipefail

      CONTAINER_NAME=chromium_001
      CF_CONTAINER=cloudflared_chromium
      IMAGE=lscr.io/linuxserver/chromium:latest
      PORT=$${PORT:-3010}   # ✅ ESCAPED agar tidak diinterpolasi oleh Nix
      TZ=Asia/Singapore
      LANG=en_US.UTF-8
      HOME_DIR="$HOME"
      DATA_DIR="$HOME_DIR/chromium_001"
      URL_FILE="$HOME_DIR/chromium_tunnel_url.txt"

      echo "=== [INIT] Chromium persistent setup ==="

      mkdir -p "$DATA_DIR"

      # Pastikan Docker aktif
      if ! docker info >/dev/null 2>&1; then
        echo "[docker] docker not running, starting dockerd manually..."
        sudo dockerd >/tmp/dockerd.log 2>&1 &
        sleep 3
      fi

      # Pull image jika belum ada
      docker image inspect "$IMAGE" >/dev/null 2>&1 || docker pull "$IMAGE"
      docker image inspect cloudflare/cloudflared:latest >/dev/null 2>&1 || docker pull cloudflare/cloudflared:latest

      # Buat network untuk komunikasi antar container
      docker network create chromium_net >/dev/null 2>&1 || true

      # Jalankan Chromium container
      if ! docker ps -a --format '{{.Names}}' | grep -qx "$CONTAINER_NAME"; then
        echo "[docker] creating Chromium container..."
        docker run -d \
          --name "$CONTAINER_NAME" \
          --network chromium_net \
          --security-opt seccomp=unconfined \
          -e PUID=1000 \
          -e PGID=1000 \
          -e TZ="$TZ" \
          -e LANG="$LANG" \
          -e LC_ALL="$LANG" \
          -e CHROME_CLI="http://localhost:3000" \
          -v "$DATA_DIR":/config \
          -p $${PORT}:3000 \   # ✅ ESCAPED agar bash yang memproses, bukan Nix
          --shm-size="1gb" \
          --restart unless-stopped \
          "$IMAGE"
      else
        docker start "$CONTAINER_NAME" || true
      fi

      # Jalankan Cloudflared (container persistent)
      if ! docker ps -a --format '{{.Names}}' | grep -qx "$CF_CONTAINER"; then
        echo "[cloudflared] starting new tunnel container..."
        docker run -d \
          --name "$CF_CONTAINER" \
          --network chromium_net \
          --restart unless-stopped \
          cloudflare/cloudflared:latest tunnel --no-autoupdate --url http://chromium_001:3000
      else
        docker start "$CF_CONTAINER" || true
      fi

      # Tunggu sampai tunnel URL siap
      echo "[cloudflared] waiting for tunnel URL..."
      URL=""
      for i in $(seq 1 60); do
        URL=$(docker logs "$CF_CONTAINER" 2>&1 | grep -oE "https://[a-z0-9.-]+trycloudflare.com" | head -n1 || true)
        [ -n "$URL" ] && break
        sleep 1
      done

      if [ -n "$URL" ]; then
        echo "$URL" > "$URL_FILE"
        echo "========================================="
        echo " 🌍 Cloudflared tunnel is active!"
        echo "     $URL"
        echo "📁 Saved to: $URL_FILE"
        echo "========================================="
      else
        echo "❌ Cloudflared URL not found — check logs:"
        echo "   docker logs $CF_CONTAINER | grep trycloudflare"
      fi

      echo "✅ Chromium container running persistently"
      echo "✅ Cloudflared auto-restart enabled"
      echo "📦 Both survive even if IDX/browser is closed"
    '';
  };

  idx.previews = {
    enable = true;
    previews = {
      chromium = {
        manager = "web";
        command = [
          "bash" "-lc"
          "socat TCP-LISTEN:3010,fork,reuseaddr TCP:127.0.0.1:3010"
        ];
      };
    };
  };
}
