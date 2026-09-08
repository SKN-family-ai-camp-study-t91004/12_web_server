"""

- 동기 요청 중심의 WSGI 서버가 Django를 불러오는 배포 진입점
  == 클라이언트 요청이 들어왔다 응답이 나가는 곳

WSGI config for _01_django_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_01_django_project.settings')

application = get_wsgi_application()
