FROM python:3.12-slim
WORKDIR /task
RUN pip install --no-cache-dir anthropic
COPY . /task
RUN chmod +x run.sh run_all.sh tests/test_verifier.sh && python3 make_scenarios.py
ENV SCENARIO=01_html_comment AGENT=naive
ENTRYPOINT ["./run.sh"]
