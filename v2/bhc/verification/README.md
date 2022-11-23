# Advanced model distribution
모델 존재 여부 검증 및 상황에 맞는 스크립트 전달 및 수행

### REF. 구축 · 배포 전 과정 흐름 도식
```mermaid
graph TD
a((USER)) -->|request|b((SERVER))
b --> |reg_url, arch, task|i([verify.py])
i --- |repo_list|c{VERIFICATION}
c --> |True|d([docker pull])
c --> |False|e([copy.yaml, autorun.yaml])
e --> |model.tar.gz|f((BUILDERS))
f --> |push new model image|h
h((registry)) --> |model_image|a
d --> h
```
