
build:
		docker build -t dvc:latest .

run:
		docker run --runtime nvidia --rm --privileged \
			--network host \
			--workdir /app/github_actions/DVC \
			--volume ~/github_actions/DVC:/app/github_actions/DVC \
			--name dvc \
			dvc:latest
