import os
import base64
import hashlib
from django.db.models import F, Q
from planetstack.config import Config
from observer.openstacksyncstep import OpenStackSyncStep
from core.models.user import User
from core.models.controllerusers import  ControllerUser
from observer.steps.sync_controller_users import SyncControllerUser

class SyncUsers(OpenStackSyncStep):
    provides=[User]
    requested_interval=0

    def sync_record(self, user):
        for controller_user in ControllerUser.objects.filter(user=user):
            # bump the 'updated' field so user account are updated across 
            # controllers.
            controller_user.save()

    def delete_record(self, user):
        controller_user_deleter = SyncControllerUser().delete_record
        for controller_user in ControllerUser.objects.filter(user=user):
            controller_user_deleter(controller_user)
