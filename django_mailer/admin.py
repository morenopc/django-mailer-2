from django.contrib import admin
from django_mailer import models


class Message(admin.ModelAdmin):
    list_display = ('to_address', 'subject', 'from_address', 'date_created')
    list_filter = ('date_created',)
    search_fields = ('to_address', 'subject', 'from_address', 'encoded_message',)
    date_hierarchy = 'date_created'
    ordering = ('-date_created',)
    list_filter = ('from_address',)


class MessageRelatedModelAdmin(admin.ModelAdmin):
    list_select_related = True

    def message__to_address(self, obj):
        return obj.message.to_address
    message__to_address.admin_order_field = 'message__to_address'
    
    def message__from_address(self, obj):
        return obj.message.from_address
    message__from_address.admin_order_field = 'message__from_address'

    def message__subject(self, obj):
        return obj.message.subject
    message__subject.admin_order_field = 'message__subject'
    
#    def message__hold(self, obj):
#        return obj.message.hold
#    message__hold.admin_order_field = 'message__hold'

    def message__date_created(self, obj):
        return obj.message.date_created.strftime('%B %e, %Y, %I:%M %P')
    message__date_created.admin_order_field = 'message__date_created'


class QueuedMessage(MessageRelatedModelAdmin):
    def not_deferred(self, obj):
        return not obj.deferred
    not_deferred.boolean = True
    not_deferred.admin_order_field = 'deferred'

    list_display = ('id', 'message__to_address', 'message__subject', 'message__from_address',
                    'message__date_created', 'priority', 'not_deferred','hold')
    list_filter = ('message__from_address',)

class Blacklist(admin.ModelAdmin):
    list_display = ('email', 'date_added')


class Log(MessageRelatedModelAdmin):
    list_display = ('id', 'result', 'message__to_address', 'message__subject',
                    'message__from_address', 'date')
    list_filter = ('result','message__from_address')
    list_display_links = ('id', 'result')


admin.site.register(models.Message, Message)
admin.site.register(models.QueuedMessage, QueuedMessage)
admin.site.register(models.Blacklist, Blacklist)
admin.site.register(models.Log, Log)
