
build:
		docker build -t dvc:latest .

run:
		docker run --rm \
			--network host \
			--workdir /app/github_actions/DVC \
			--volume ~/github_actions/DVC:/app/github_actions/DVC \
			--name dvc \
			dvc:latest

debug:
		docker run -it --rm \
			--network host \
			--volume /home/inoue/.ssh:/tmp/.ssh:ro \
			--volume /home/inoue/.zshrc:/tmp/.zshrc:ro \
			--volume /home/inoue/.tmux.conf:/tmp/.tmux.conf:ro \
			--workdir /app/github_actions/DVC \
			--volume ~/github_actions/DVC:/app/github_actions/DVC \
			--name dvc \
			dvc:latest
