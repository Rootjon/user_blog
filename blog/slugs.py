from genericpath import exists
from pyexpat import model
import random
import string
from django.utils.text import slugify

def genaret_unique_slug(instance, base_title, new_slug=False, update=False):
    slug=slugify(base_title)
    model = instance.__class__
    if new_slug:
        slug=new_slug
    if update:
        slug_exist=model.objects.filter(
        slug__icontains=slug
    ).exclude(pk=instance.pk)

    else:
        slug_exist=model.objects.filter(
        slug__icontains=slug
    ).exists()

    if slug_exist:
        random_string="".join(random.choices(string.ascii_lowercase, k=4))
        new = slugify(base_title +'_'+ random_string)
        return genaret_unique_slug(
            instance,
            base_title,
            new_slug=new
        )
    return slug