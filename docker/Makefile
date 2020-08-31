
build:
		docker build -t dvc:run .

repro:
		docker run --rm \
			--network host \
			--workdir /app/github_actions/DVC \
			--volume ~/github_actions/DVC:/app/github_actions/DVC \
			--volume ~/github_actions/dvc_storage:/app/github_actions/dvc_storage \
			dvc:latest \
			entrypoint_repro.sh

debug:
		docker run -it --rm \
			--network host \
			--workdir /app/github_actions/DVC \
			--volume /home/inoue/.ssh:/tmp/.ssh:ro \
			--volume /home/inoue/.zshrc:/tmp/.zshrc:ro \
			--volume /home/inoue/.tmux.conf:/tmp/.tmux.conf:ro \
			--volume ~/github_actions/DVC:/app/github_actions/DVC \
			--volume ~/github_actions/dvc_storage:/app/github_actions/dvc_storage \
			--name dvc \
			dvc:latest \
			entrypoint_debug.sh
