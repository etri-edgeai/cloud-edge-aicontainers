# pytorch 를 이용한 분산학습

## 전통적인 분산학습

- 다음과 같은 분산 시스템의 적절한 설정은 매우 중요
- 클러스터를 구성하는 공통 네트워크에 연결된 노드 집합
- InfiniBand와 같은 고대역폭 네트워크와 노드로 고급 서버를 사용하는 것 추천
- 비밀번호 없는 SSH 그들 사이의 연결성 (원활한 연결에 매우 중요)
- MPI 구현을 설치해야 함
- 공통 파일 시스템 이 노드는 모든 노드에서 볼 수 있어야 하며 분산 응용 프로그램은 해당 노드에 있어야 함 (네트워크 파일 시스템(NFS) 이것을 달성하는 한 가지 방법)


