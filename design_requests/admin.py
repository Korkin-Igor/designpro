from django.contrib import admin

from design_requests.models import DesignRequest, Category, CustomUser

admin.site.register(Category)
admin.site.register(DesignRequest)
admin.site.register(CustomUser)