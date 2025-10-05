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
      PORT=${PORT:-3010}
      TZ=Asia/Singapore
      LANG=en_US.UTF-8
      DATA_DIR=/home/user/chromium_001
      URL_FILE=/home/user/chromium_tunnel_url.txt

      echo "=== [INIT] Starting persistent Chromium workspace ==="

      mkdir -p "$DATA_DIR"

      # Pastikan Docker aktif
      if ! systemctl is-active --quiet docker; then
        echo "[docker] service not active, attempting to start..."
        sudo systemctl start docker || true
      fi

      # Pull image jika belum ada
      docker image inspect "$IMAGE" >/dev/null 2>&1 || {
        echo "[docker] pulling $IMAGE..."
        docker pull "$IMAGE"
      }

      # Jalankan container Chromium
      if ! docker ps -a --format '{{.Names}}' | grep -qx "$CONTAINER_NAME"; then
        echo "[docker] creating new Chromium container..."
        docker run -d \
          --name "$CONTAINER_NAME" \
          --security-opt seccomp=unconfined \
          -e PUID=1000 \
          -e PGID=1000 \
          -e TZ="$TZ" \
          -e LANG="$LANG" \
          -e CHROME_CLI="http://localhost:${PORT}" \
          -v "$DATA_DIR":/config \
          -p ${PORT}:3000 \
          --shm-size="1gb" \
          --restart unless-stopped \
          "$IMAGE"
      else
        echo "[docker] ensuring Chromium container is running..."
        docker start "$CONTAINER_NAME" >/dev/null || true
      fi

      # Jalankan Cloudflared via Docker container (persistent)
      if docker ps -a --format '{{.Names}}' | grep -qx "$CF_CONTAINER"; then
        echo "[cloudflared] restarting existing tunnel container..."
        docker restart "$CF_CONTAINER" >/dev/null
      else
        echo "[cloudflared] creating new tunnel container..."
        docker run -d \
          --name "$CF_CONTAINER" \
          --restart unless-stopped \
          --network host \
          cloudflare/cloudflared:latest tunnel --no-autoupdate --url http://localhost:${PORT}
      fi

      echo "[cloudflared] waiting for tunnel URL..."
      sleep 10

      URL=$(docker logs "$CF_CONTAINER" 2>&1 | grep -oE "https://[a-z0-9.-]+trycloudflare.com" | head -n1 || true)

      if [ -n "$URL" ]; then
        echo "$URL" > "$URL_FILE"
        echo "========================================="
        echo " 🌍 Cloudflared tunnel is active!"
        echo "     $URL"
        echo "📁 Saved to: $URL_FILE"
        echo "========================================="
      else
        echo "❌ Cloudflared URL not found — check logs with:"
        echo "   docker logs $CF_CONTAINER | grep trycloudflare"
      fi

      echo "✅ Chromium container: $CONTAINER_NAME"
      echo "✅ Tunnel container:   $CF_CONTAINER"
      echo "📦 Both are set to restart automatically."

      # Jangan tahan sesi IDX; biarkan kembali ke prompt
      echo "[info] Background services are now persistent — safe to close browser."
    '';
  };

  idx.previews = {
    enable = true;
    previews = {
      chromium = {
        manager = "web";
        command = [
          "bash" "-lc"
          "socat TCP-LISTEN:${PORT},fork,reuseaddr TCP:127.0.0.1:3010"
        ];
      };
    };
  };
}
