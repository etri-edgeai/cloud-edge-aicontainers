# push_dockerhub

- 1개의 애플리케이션을 두 개의 다른 아키텍처(ARM 기반의 라즈베리파이, x86 기반의 일반 PC)를 지원하는 컨테이너 이미지로 빌드합니다.
- 이를 위해 Docker의 멀티 아키텍처 빌드 기능을 사용합니다.
- 이 작업은 Docker의 buildx 기능을 사용하면 가능합니다.
- 본 예제에서는 Python 애플리케이션 app.py를 ARM과 x86 아키텍처를 모두 지원하는 컨테이너 이미지로 빌드하고, 도커 허브에 push 합니다.
