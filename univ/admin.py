from django.contrib import admin

from univ.models import University, MajorBlock, Jeonhyeong, Schedule


admin.site.register(University)
admin.site.register(MajorBlock)
admin.site.register(Jeonhyeong)
admin.site.register(Schedule)

