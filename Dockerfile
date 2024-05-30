FROM pytorch/conda-cuda:latest



USER root

COPY  env.yaml /tmp/env.yaml
COPY  requirements.txt /tmp/requirements.txt
RUN conda install -y -n llm -f /tmp/env.yaml 
COPY --chmod=755 run.sh /tapis/run.sh

COPY  create-Knowledge-graph.py create-Knowledge-graph.py
COPY  requirements.txt /tmp/requirements.txt

ENV PATH="/opt/conda/bin:${PATH}"
ENV PATH "/code:$PATH"
ENTRYPOINT [ "run.sh" ]