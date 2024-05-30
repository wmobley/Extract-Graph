FROM nvidia/cuda:12.3.2-runtime-ubi8



USER root

COPY --chown=$root:$root env.yaml /tmp/env.yaml
COPY --chown=$root:$root requirements.txt /tmp/requirements.txt
RUN conda install -y -n llm -f /tmp/env.yaml 
COPY --chmod=755 run.sh /tapis/run.sh

COPY --chown=$root:$root create-Knowledge-graph.py create-Knowledge-graph.py
COPY --chown=$root:$root requirements.txt /tmp/requirements.txt

ENV PATH="/opt/conda/bin:${PATH}"
ENV PATH "/code:$PATH"
ENTRYPOINT [ "run.sh" ]