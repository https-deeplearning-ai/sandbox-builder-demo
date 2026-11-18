build:
	docker build --platform=linux/amd64 -f Dockerfile . -t public.ecr.aws/deeplearning-ai/public-courses:ttyd-V1
	docker push public.ecr.aws/deeplearning-ai/public-courses:ttyd-V1


run:
	docker run --rm -p 8888:8888 public.ecr.aws/deeplearning-ai/public-courses:ttyd-V1
