## About The Project
This repo collects the following lectures to demonstrate the usage of sandbox builder:
- L2: anthropic support, real lesson from MCP: Build Rich-Context AI Apps with Anthropic
- assignments/L1: example of coding assignments

## Common Directory Structures
```
├── L2
│   ├── L_2.ipynb
│   ├── helper.py
│   ├── mentions-processed.csv
│   └── requirements.txt
├── assignments
│   └── L1
│       ├── SIMPLE_DEMO_L1_Assignment.ipynb
│       └── autograder
│           ├── Dockerfile
│           ├── Makefile
│           ├── entry.py
│           ├── grader.py
│           ├── requirements.txt
│           └── ...
├── services
│   ├── exa.ipynb
│   ├── openai_.ipynb
│   ├── tavily_.ipynb
│   └── together.ipynb
├── sidecar-pg
│   ├── connect_to_postgres.ipynb
│   ├── docker-compose.yml
│   └── requirements.txt
├── sidecar-redis
│   ├── connect_to_redis.ipynb
│   ├── docker-compose.yml
│   └── requirements.txt
├── README.md
└── requirements.txt
```

## Proxy Environment variables


## testing
- EXA_BASE_URL=http://jupyter-api-proxy.stg.internal.dlai/rev-proxy/exa EXA_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcHAiLCJleHAiOjE3OTk5OTk5OTksInN1YiI6NDc5LCJhdWQiOiJXRUIiLCJpYXQiOjE2OTQwNzY4NTF9.5upFqaJKhBD82QcdJ2ipzgDHV_oZARUpzeD1xoTPXCI uv run jupyter lab
