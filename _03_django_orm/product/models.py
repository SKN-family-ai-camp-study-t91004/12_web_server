from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Discount(models.Model):
    # Discount ---> Product (1:1 관계)
    # on_delete=models.CASCADE:
    # - 참조하던 부모(Product)가 삭제되면 자식(Discount)도 삭제
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name='discount',
    )
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2,
        help_text='Discount ratio (e.g., 0.10 for 10%)',
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f'{self.discount_percentage * 100}% off for {self.product.name}'


class Review(models.Model):
    # Review ---> Product (N:1 관계)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews',
    )
    user_id = models.PositiveIntegerField(blank=True, null=True)
    rating = models.PositiveIntegerField(default=1, help_text='Rating from 1 to 5')
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.product.name} by {self.user_id}'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    # Category ---> Product (N:M 관계)
    # -> 중간 테이블(중간 모델) 생성 해서 N:M 관계를 해소
    # -> Category ---> Category_Product <--- Product
    #            (1:N)                 (M:1)
    products = models.ManyToManyField(Product, related_name='categories', blank=True)

    def __str__(self):
        return self.name
