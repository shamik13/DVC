
build_repro:
		docker build -t dvc:repro --build-arg ENTRYPOINT_SCRIPT=entrypoint_repro.sh .

build_debug:
		docker build -t dvc:debug --build-arg ENTRYPOINT_SCRIPT=entrypoint_debug.sh .

run_repro:
		docker run --rm \
			--network host \
			--workdir /app/DVC \
			--volume ~/github/DVC:/app/DVC \
			dvc:repro \
			entrypoint_repro.sh

run_debug:
		docker run -it --rm \
			--network host \
			--workdir /app/DVC \
			--volume ~/.ssh:/tmp/.ssh:ro \
			--volume ~/.zshrc:/tmp/.zshrc:ro \
			--volume ~/.tmux.conf:/tmp/.tmux.conf:ro \
			--volume ~/github/DVC:/app/DVC \
			--name dvc_debug \
			--hostname dvc_debug \
			dvc:debug
