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

      CLEAN_MARK=/home/user/.cleanup_done
      CONTAINER_NAME=chromium_001
      IMAGE=lscr.io/linuxserver/chromium:latest
      PORT=${PORT:-3010}
      TZ=Asia/Singapore
      LANG=en_US.UTF-8

      # One-time cleanup (opsional)
      if [ ! -f "$CLEAN_MARK" ]; then
        echo "[init] performing one-time cleanup..."
        rm -rf /home/user/.gradle/* /home/user/.emu/* || true
        find /home/user -mindepth 1 -maxdepth 1 ! -name 'idx-ubuntu22-gui' ! -name '.*' -exec rm -rf {} + || true
        touch "$CLEAN_MARK"
      fi

      # Pull image (jika belum ada)
      if ! docker image inspect "$IMAGE" > /dev/null 2>&1; then
        echo "[docker] pulling $IMAGE..."
        docker pull "$IMAGE"
      fi

      # Jalankan Cloudflared untuk membuat tunnel ke localhost:$PORT
      CF_LOG=/tmp/cloudflared.$(date +%s).log
      echo "[cloudflared] starting tunnel on port $PORT (log: $CF_LOG)"
      nohup cloudflared tunnel --no-autoupdate --url http://localhost:${PORT} > "$CF_LOG" 2>&1 &

      # Tunggu sampai URL Cloudflare muncul
      URL=""
      echo "[cloudflared] waiting for tunnel..."
      for i in $(seq 1 20); do
        if grep -q "trycloudflare.com" "$CF_LOG"; then
          URL=$(grep -oE "https://[a-z0-9.-]+trycloudflare.com(:[0-9]+)?" "$CF_LOG" | head -n1 || true)
          break
        fi
        sleep 1
      done

      if [ -n "$URL" ]; then
        echo "========================================="
        echo " 🌍 Cloudflared tunnel ready!"
        echo "     $URL"
        echo "========================================="
      else
        echo "❌ Cloudflared tunnel failed or not ready within timeout."
        echo "Check log: $CF_LOG"
        URL="http://localhost:${PORT}"  # fallback
      fi

      # Buat volume folder
      mkdir -p /home/user/chromium_001

      # Buat container Chromium jika belum ada
      if ! docker ps -a --format '{{.Names}}' | grep -qx "$CONTAINER_NAME"; then
        echo "[docker] creating new container: $CONTAINER_NAME"
        docker run -d \
          --name "$CONTAINER_NAME" \
          --security-opt seccomp=unconfined \
          -e PUID=1000 \
          -e PGID=1000 \
          -e TZ="$TZ" \
          -e LANG="$LANG" \
          -e CHROME_CLI="$URL" \
          -v /home/user/chromium_001:/config \
          -p ${PORT}:3000 \
          --shm-size="1gb" \
          --restart unless-stopped \
          "$IMAGE"
      else
        echo "[docker] starting existing container: $CONTAINER_NAME"
        docker start "$CONTAINER_NAME" || true
      fi

      echo "✅ Chromium container running on port $PORT"
      echo "🌍 Accessible at: $URL"

      # Keep workspace alive
      elapsed=0
      while true; do
        echo "[heartbeat] chromium running — ${elapsed} min elapsed"
        elapsed=$((elapsed + 1))
        sleep 60
      done
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
