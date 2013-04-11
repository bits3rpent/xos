from plstackapi.openstack.client import OpenStackClient
from plstackapi.openstack.driver import OpenStackDriver
from plstackapi.core.api.auth import auth_check
from plstackapi.core.models import Role
 

def add_role(auth, name):
    driver = OpenStackDriver(client = auth_check(auth))    
    keystone_role = driver.create_role(name=name)
    role = Role(role_type=name, role_id=keystone_role.id)
    role.save()
    return role

def delete_role(auth, filter={}):
    driver = OpenStackDriver(client = auth_check(auth))   
    roles = Role.objects.filter(**filter)
    for role in roles:
        driver.delete_role({'id': role.role_id}) 
        role.delete()
    return 1

def get_roles(auth, filter={}):
    client = auth_check(auth)
    roles = Role.objects.filter(**filter)
    return roles             
        

    