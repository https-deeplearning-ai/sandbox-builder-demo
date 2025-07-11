FROM python:3.12
USER root

COPY ./requirements.txt .
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
RUN uv pip install --system --no-cache-dir -r requirements.txt

RUN chsh -s /bin/bash
RUN useradd jovyan -d /home/jovyan -m -p 0049e6b11c44d4b00006eb820983a7a76c84a12d -s /bin/bash && \
    echo "jovyan ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers && \
    chmod -R 755 /usr/local/share/jupyter && \
    usermod -u 1100 jovyan && groupmod -g 3000 jovyan && \
    jupyter server --generate-config && \
    mkdir -p /home/jovyan/work

COPY ./jupyter_server_config.py /home/jovyan/.jupyter/jupyter_server_config.py

COPY ./L2 /home/jovyan/work/L2
COPY ./L3 /home/jovyan/work/L3

RUN chown -R jovyan:jovyan -R /home/jovyan
RUN chown -R jovyan:jovyan -R /home/jovyan/work

USER jovyan
CMD ["bash", "-c", "source /etc/bash.bashrc && jupyter notebook --no-browser"]
