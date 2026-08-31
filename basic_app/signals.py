from pathlib import Path

from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image, UnidentifiedImageError

from .models import (
    About,
    Activity,
    Blog,
    BoardMember,
    Category,
    Event,
    ExecutiveCommittee,
    Gallery,
    GalleryImage,
    SiteSettings,
    Slider,
    Training,
)


IMAGE_FIELDS = {
    About: ("image", "og_image"),
    Activity: ("image", "og_image"),
    Blog: ("featured_image", "og_image"),
    BoardMember: ("photo",),
    Category: ("og_image",),
    Event: ("poster", "og_image"),
    ExecutiveCommittee: ("photo",),
    Gallery: ("cover_image", "og_image"),
    GalleryImage: ("image",),
    SiteSettings: ("logo", "favicon", "og_image"),
    Slider: ("image",),
    Training: ("image", "og_image"),
}


def resize_image_file(file_field, max_size=(1400, 1400), quality=85):
    if not file_field:
        return

    image_path = Path(file_field.path)
    if not image_path.exists():
        return

    try:
        with Image.open(image_path) as image:
            image.verify()
        with Image.open(image_path) as image:
            if image.width <= max_size[0] and image.height <= max_size[1]:
                return
            image.thumbnail(max_size)
            save_kwargs = {"quality": quality, "optimize": True}
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")
            image.save(image_path, **save_kwargs)
    except (OSError, UnidentifiedImageError, ValueError):
        return


@receiver(post_save)
def resize_uploaded_images(sender, instance, **kwargs):
    field_names = IMAGE_FIELDS.get(sender)
    if not field_names:
        return
    for field_name in field_names:
        resize_image_file(getattr(instance, field_name, None))
