from accounts.models import Trainee


def is_trainee(user):
    t = user.type
    if t == 'R' or t == 'C' or t == 'S':
        return True
    return False

def is_TA(user):
    t = user.type
    if t == 'T':
        return True
    return False

def trainee_from_user(user):
    try:
        return Trainee.objects.get(id=user.id)
    except Trainee.DoesNotExist:
        return None


