from django.db import models
from django.utils import timezone


class ModelWithImageAndOrder(models.Model):
    class Meta:
        abstract = True

    image = models.ImageField(blank=True, null=True, verbose_name='картинка')
    order = models.PositiveSmallIntegerField(
        default=100, verbose_name='порядок')


class CategoryManager(models.Manager):
    def top_level(self):
        qs = self.filter(parent__isnull=False)
        return qs.filter(
            parent__parent__isnull=True).order_by('parent')


class Category(ModelWithImageAndOrder):
    objects = CategoryManager()

    class Meta:
        verbose_name = 'категорія'
        verbose_name_plural = 'категорії'
        ordering = ['order']

    name = models.CharField(verbose_name="назва", max_length=200)
    parent = models.ForeignKey(
        "self", null=True, blank=True,
        related_name="children", on_delete=models.CASCADE,
        verbose_name='верхня категорія'
    )

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        name_list = [self.name]
        obj = self
        already_visited = [obj]
        while (obj := obj.parent) is not None and obj not in already_visited:
            already_visited.append(obj)
            name_list.append(obj.name)
        return '->'.join(reversed(name_list))
    full_name.fget.short_description = 'назва'

    def collect_children(self):
        """Get all child categories including self."""
        result = [self]
        children = Category.objects.filter(parent=self)
        for child in children:
            result.extend(child.collect_children())
        return result

    def get_root_parent(self):
        """Get the root parent category."""
        if self.parent is None:
            return self
        return self.parent.get_root_parent()

    @property
    def root_category(self):
        """Get the root parent category name."""
        return self.get_root_parent().name
    root_category.fget.short_description = 'базова категорія'

    def get_all_products(self):
        """Get all products in this category and its children."""
        products = [
            product
            for category in self.collect_children()
            for product in category.products.all()
        ]
        return products


class ReceiptManager(models.Manager):
    def actual(self):
        today = timezone.now().date()
        return self.filter(created_at__date=today)


class Receipt(models.Model):
    objects = ReceiptManager()

    class Meta:
        verbose_name = 'чек'
        verbose_name_plural = 'чеки'
        ordering = ('created_at',)

    class PaymentMethod(models.TextChoices):
        CARD = 'CARD', 'Картка'
        CASH = 'CASH', 'Готівка'
        CARD_TRANSFER = 'CARD_TRANSFER', 'Переказ на картку'

    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Відкритий'
        CLOSED = 'CLOSED', 'Зaкритий'

    number = models.PositiveIntegerField(
        verbose_name='номер', null=True, blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='дата створення')

    updated_at = models.DateTimeField(
        verbose_name='дата оновлення', default=timezone.now)

    place = models.ForeignKey('place.Place',
                              null=True, blank=True,
                              verbose_name='місце', on_delete=models.SET_NULL)
    payment_method = models.CharField(
        max_length=50, choices=PaymentMethod, default=PaymentMethod.CARD)
    status = models.CharField(
        max_length=10, choices=Status, default=Status.OPEN)

    def __str__(self):
        return f'{self.id}' if self.number is None else str(self.number)

    @property
    def price(self):
        return sum(
            [p.total_cost for p in self.product_items.all()]
        )


class Product(ModelWithImageAndOrder):
    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукти'
    name = models.CharField(verbose_name="назва", max_length=300)
    price = models.DecimalField(
        verbose_name='ціна', max_digits=6, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='категорія',
        related_name='products')

    def __str__(self):
        return self.name


class ProductItem(models.Model):
    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукти"

    product_type = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='продукт', related_name='product_items')
    receipt = models.ForeignKey(
        Receipt, on_delete=models.CASCADE, verbose_name='чек', related_name='product_items')
    amount = models.PositiveSmallIntegerField(
        verbose_name='кількість')
    name = models.CharField(verbose_name='назва',
                            max_length=200, null=True, blank=True)
    total_cost = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False)

    def __str__(self):
        return self.product_type.name

    def save(self, *args, **kw):
        self.total_cost = self.get_total_cost()
        super().save(*args, **kw)

    def get_total_cost(self):
        return self.amount * self.product_type.price
