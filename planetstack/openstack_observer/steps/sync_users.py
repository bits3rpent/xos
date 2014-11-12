import os
import base64
import hashlib
from django.db.models import F, Q
from planetstack.config import Config
from observer.openstacksyncstep import OpenStackSyncStep
from core.models.user import User
from core.models.userdeployments import  UserDeployment
from observer.steps.sync_user_deployments import SyncUserDeployment

class SyncUsers(OpenStackSyncStep):
    provides=[User]
    requested_interval=0

    def sync_record(self, user):
        for user_deployment in UserDeployment.objects.filter(user=user):
            # bump the 'updated' field so user account are updated across 
            # deployments.
            user_deployment.save()

    def delete_record(self, user):
        user_deployment_deleter = SyncUserDeployment().delete_record
        for user_deployment in UserDeployment.objects.filter(user=user):
            user_deployment_deleter(user_deployment)
