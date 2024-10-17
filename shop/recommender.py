import redis
from django.conf import settings
from .models import Product

# Connect to Redis
r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)


class Recommender:
    """A class to provide product recommendations based on purchase history.

    This class uses Redis to store and retrieve information about products
    purchased together, allowing for the suggestion of related products
    to users.
    """

    def get_product_key(self, id):
        """Get the Redis key for products purchased together with the given product ID.

        Args:
            id (int): The product ID.

        Returns:
            str: The Redis key for the specified product's purchase relationships.
        """
        return f'product:{id}:purchased_with'

    def products_bought(self, products):
        """Record the products bought together with each product in Redis.

        This method iterates over the provided products and increments the
        score for each product pair, indicating that they were purchased
        together.

        Args:
            products (list): A list of Product instances that were purchased together.
        """
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                if product_id != with_id:
                    r.zincrby(
                        self.get_product_key(product_id), 1, with_id
                    )

    def suggest_products_for(self, products, max_results=6):
        """Suggest products based on the products provided.

        This method retrieves products that are commonly purchased together
        with the given products, using their purchase history stored in Redis.

        Args:
            products (list): A list of Product instances for which to generate recommendations.
            max_results (int): The maximum number of suggested products to return.

        Returns:
            list: A list of Product instances recommended for the given products.
        """
        product_ids = [p.id for p in products]
        if len(products) == 1:
            # Only 1 product
            suggestions = r.zrange(
                self.get_product_key(product_ids[0]), 0, -1, desc=True
            )[:max_results]
        else:
            # Generate a temporary key
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = f'tmp_{flat_ids}'
            # Multiple products, combine scores of all products
            # Store the resulting sorted set in a temporary key
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)
            # Remove ids for the products the recommendation is for
            r.zrem(tmp_key, *product_ids)
            # Get the product ids by their score, descendant sort
            suggestions = r.zrange(
                tmp_key, 0, -1, desc=True
            )[:max_results]
            # Remove the temporary key
            r.delete(tmp_key)
        suggested_products_ids = [int(id) for id in suggestions]
        # Get suggested products and sort by order of appearance
        suggested_products = list(
            Product.objects.filter(id__in=suggested_products_ids)
        )
        suggested_products.sort(
            key=lambda x: suggested_products_ids.index(x.id)
        )
        return suggested_products

    def clear_purchases(self):
        """Clear all purchase records from Redis for all products.

        This method deletes the Redis keys associated with products,
        effectively clearing the recorded purchase history.
        """
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))
