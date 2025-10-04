{ pkgs, ... }: {
  channel = "stable-24.11";

  packages = with pkgs; [
    docker
    cloudflared
    socat
    coreutils
    gnugrep
  ];

  services.docker.enable = true;

  idx.workspace.onStart = {
    novnc = ''
      set -e

      if [ ! -f /home/user/.cleanup_done ]; then
        rm -rf /home/user/.gradle/* /home/user/.emu/* || true
        find /home/user -mindepth 1 -maxdepth 1 ! -name 'idx-ubuntu22-gui' ! -name '.*' -exec rm -rf {} +
        touch /home/user/.cleanup_done
      fi

      docker ps -aq | xargs -r docker stop
      docker ps -aq | xargs -r docker rm
      docker images -q | xargs -r docker rmi -f
      docker volume prune -f
      docker network prune -f

      docker run -d --name otohits -e APPLICATION_KEY=14e755f0-a345-4c5f-b15b-b65ec94195a1 otohits/app:latest
      docker run -d --name feelingsurf -e access_token=75b30332c0b6dbca7150b9baabe020f5 feelingsurf/viewer:stable
    '';
  };

  idx.previews = {
    enable = true;
    previews = {
      novnc = {
        manager = "web";
        command = [
          "bash" "-lc"
          "socat TCP-LISTEN:$PORT,fork,reuseaddr TCP:127.0.0.1:8080"
        ];
      };
    };
  };
}
