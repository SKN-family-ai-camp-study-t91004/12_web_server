"""

- 비동기 요청 중심의 ASGI 서버가 Django를 불러오는 배포 진입점

ASGI config for _01_django_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_01_django_project.settings')

application = get_asgi_application()
