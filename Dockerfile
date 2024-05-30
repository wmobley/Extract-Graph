FROM nvidia/cuda:12.3.2-runtime-ubi8



USER root
RUN apt-get update && apt-get install -y 
    
USER mambauser

COPY --chown=$MAMBA_USER:$MAMBA_USER env.yaml /tmp/env.yaml
COPY --chown=$MAMBA_USER:$MAMBA_USER requirements.txt /tmp/requirements.txt
RUN micromamba install -y -n llm -f /tmp/env.yaml 
COPY --chmod=755 run.sh /tapis/run.sh

COPY --chown=$MAMBA_USER:$MAMBA_USER create-Knowledge-graph.py create-Knowledge-graph.py
COPY --chown=$MAMBA_USER:$MAMBA_USER requirements.txt /tmp/requirements.txt

ENV PATH="/opt/conda/bin:${PATH}"
ENV PATH "/code:$PATH"
ENTRYPOINT [ "run.sh" ]