# root계정으로 접속

# 사용자 django/django 생성
create user 'django'@'%' identified by 'django';


# djangodb 데이터베이스 생성
# - 인코딩 utf8mb4 (다국어/이모지 텍스트 지원)
# - 정렬방식 utf8mb4_unicode_ci (대소문자 구분없음)
create database djangodb character set utf8mb4 collate utf8mb4_unicode_ci;

# django 계정 권한 부여
grant all privileges on djangodb.* to 'django'@'%';
flush privileges;