from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """읽기는 공개하고 변경은 작성자에게만 허용한다. staff도 다른 글은 변경하지 않는다."""
    def has_object_permission(self, request, view, obj):
        # GET/HEAD/OPTIONS는 공개한다. PATCH/DELETE 등은 조회한 객체의 author_id와 요청 사용자 PK를 비교한다.
        # ModelViewSet이 상세 객체를 가져올 때 이 검사를 호출한다. 목록의 행을 자동으로 걸러 주지는 않는다.
        # False이면 DRF가 변경을 거부한다. 객체가 없는 생성 요청은 IsAuthenticatedOrReadOnly가 따로 검사한다.
        return request.method in SAFE_METHODS or obj.author_id == request.user.pk