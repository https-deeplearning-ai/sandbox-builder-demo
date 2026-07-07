build:
	docker build --platform=linux/amd64 -f Dockerfile . -t public.ecr.aws/deeplearning-ai/public-courses:tau-V1
	docker push public.ecr.aws/deeplearning-ai/public-courses:tau-V1


run:
	docker run --rm -e OPENROUTER_API_KEY=$(OPENROUTER_API_KEY) -p 8888:8888 public.ecr.aws/deeplearning-ai/public-courses:tau-V1
