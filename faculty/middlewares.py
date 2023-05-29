from .models import *
from easy_thumbnails.files import get_thumbnailer


def teacher_data_context_processor(request):
    if request.user.is_authenticated:
        if request.user.teacher_image:
            try:
                thumbnail_small_url = get_thumbnailer(request.user.teacher_image)['small'].url
                thumbnail_default_url = get_thumbnailer(request.user.teacher_image)['default'].url
                return {'thumbnail_small_url': thumbnail_small_url,
                    'thumbnail_default_url': thumbnail_default_url}

            #easy thumbnail may have another problem
            except:
                print('Easy thumbnail error')
                no_image = True
                return {'thumbnail_small_url': "/media/images/avatar_default_small.png",
                        'thumbnail_default_url': "/media/images/avatar_default_default.png",
                        'no_image': no_image}
    no_image = True
    return {'thumbnail_small_url': "/media/images/avatar_default_small.png",
            'thumbnail_default_url': "/media/images/avatar_default_default.png",
            'no_image': no_image}