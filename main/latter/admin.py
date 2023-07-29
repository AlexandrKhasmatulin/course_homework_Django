from django.contrib import admin

from main.latter.models import Mailing, SmsLetter, MailingLog, Client


admin.site.register(Mailing)
admin.site.register(Client)
admin.site.register(MailingLog)
admin.site.register(SmsLetter)
