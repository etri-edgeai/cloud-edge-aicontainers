FROM nginx:latest

# 기존 설정파일 삭제
RUN rm /etc/nginx/conf.d/default.conf

# 새로운 설정파일 복사 
COPY . /usr/share/nginx/html
COPY config/conf.d/default.conf /etc/nginx/conf.d/default.conf
COPY config/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

ENTRYPOINT ["nginx","-g","daemon off;"]
