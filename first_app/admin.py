from django.contrib import admin

from .models import People
admin.site.register(People)

from .models import Account
admin.site.register(Account)

from .models import Company
admin.site.register(Company)

from .models import Employee
admin.site.register(Employee)

from .models import Tokopade
admin.site.register(Tokopade)

from .models import Player
admin.site.register(Player)
