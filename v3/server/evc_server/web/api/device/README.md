-----------------------------------------------------
# 연구노트 
 - 기술문서명 : 연동분석 프레임워크 구성을 위한 RTX3080ti 에지 디바이스
 - 과제명 : 능동적 즉시 대응 및 빠른 학습이 가능한 적응형 경량 엣지 연동분석 기술개발
 - 영문과제명 : Development of Adaptive and Lightweight Edge-Collaborative Analysis Technology for Enabling Proactively Immediate Response and Rapid Learning
 - Acknowledgement : This work was supported by Institute of Information & communications Technology Planning & Evaluation (IITP) grant funded by the Korea government(MSIT) (No. 2021-0-00907, Development of Adaptive and Lightweight Edge-Collaborative Analysis Technology for Enabling Proactively Immediate Response and Rapid Learning).
 - 작성자 : 박종빈
 
 - 날짜 : 2023-04-25
 - 연구자 : 박종빈, 박효찬
-----------------------------------------------------

## 필요성

- 기계학습은 많은 자원을 필요로 합니다.
- 예컨데 CPU, GPU, RAM과 같은 연산자원이 많이 필요하고, 네트워크 부하도 크게 발생할 수 있습니다.
- 따라서 학습과정에서 서버 및 에지 노드를 면밀히 모니터링하는 작업은 매우 중요합니다.
- 현장에서는 특정 학습 노드에 냉각팬이 고장나서 CPU와 GPU에 과열이 발생하여 시스템 성능이 급감하는 사례도 발생합니다.


## 개발 절차

- 서버에서 센서 데이터 수집: 서버에서 온도 및 CPU 상태를 모니터링하기 위해, 서버에서 데이터를 수집해야합니다. 

- 데이터 저장: 수집한 데이터를 저장하기 위해 데이터베이스를 사용할 수 있습니다. 데이터베이스는 sqlite, MySQL, PostgreSQL, MongoDB 등 다양한 유형이 있으며, 사용하고자 하는 데이터베이스에 대한 연결 설정을 수행해야 합니다.

- 웹 애플리케이션 개발: 수집된 데이터를 표시하고 시각화할 수 있는 웹 애플리케이션이 필요합니다.

- 데이터 시각화: 개발된 웹 애플리케이션에서 데이터를 시각화하는 데에는 다양한 도구와 라이브러리를 사용할 수 있습니다. 예를 들어, JavaScript의 D3.js, Plotly.js, Chart.js 등을 사용할 수 있습니다. 이를 통해 온도 및 CPU 상태와 같은 데이터를 차트, 그래프 또는 다른 시각적 표현으로 표시할 수 있습니다.

- 서버 배포: 마지막으로, 개발한 웹 애플리케이션을 서버에 배포해야 합니다. 이를 위해, 서버 운영체제에 따라 적절한 방법을 사용하여 애플리케이션을 설치하고 구성해야 합니다. 이 단계에서는 보안을 고려하여 서버에 대한 액세스 권한과 함께 웹 애플리케이션을 배포해야 합니다.

- 이러한 단계를 수행하여 원격지 서버의 온도 및 CPU 상태를 모니터링하고 시각화할 수 있습니다.


## 연구 내용

- Port 방화벽 처리 (8000번 포트를 여는 예시)

```bash
$ sudo iptables -I INPUT -p tcp --dport 8000 -j ACCEPT
$ sudo iptables -I OUTPUT -p tcp --sport 8000 -j ACCEPT
```
