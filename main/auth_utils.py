def is_employee(user):
    return user.groups.filter(name='Employee').exists() or user.is_superuser
