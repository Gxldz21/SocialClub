from multiclub.models import UserSet


def pic(request):
    if request.user.is_authenticated:
        picture = UserSet.objects.filter(user=request.user).first()
        if UserSet.objects.filter(user=request.user).exists():
            return {
                'pic': picture.avatar
            }
        else:
            return {
                'pic': None
            }
    else:
        return {
            'pic': None
        }
