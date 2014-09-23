import os
import base64
import random
from datetime import datetime
from django.db.models import F, Q
from planetstack.config import Config
from observer.openstacksyncstep import OpenStackSyncStep
from core.models.node import Node
from core.models.site import Site, Deployment
from util.logger import Logger, logging

logger = Logger(level=logging.INFO)

class SyncNodes(OpenStackSyncStep):
    provides=[Node]
    requested_interval=0

    def fetch_pending(self, deleted):
        # Nodes come from the back end
        # You can't delete them
        if (deleted):
            return []

        # collect local nodes
        sites = Site.objects.all()
        nodes = Node.objects.all()
        node_hostnames  = [node.name for node in nodes]

        # fetch all nodes from each deployment
        deployments = Deployment.objects.all()
        new_nodes = []
        for deployment in deployments:
            try:
                driver = self.driver.admin_driver(deployment=deployment.name)
                compute_nodes = driver.shell.nova.hypervisors.list()
            except:
                logger.log_exc("Failed to get nodes from deployment %s" % str(deployment))
                continue

            for compute_node in compute_nodes:
                if compute_node.hypervisor_hostname not in node_hostnames:
                    # XX TODO:figure out how to correctly identify a node's site.
                    # XX pick a random site to add the node to for now
                    site_index = random.randint(0, len(sites))
                    node = Node(name=compute_node.hypervisor_hostname,
                                site=sites[site_index], deployment=deployment)
                    new_nodes.append(node)

        return new_nodes    
                 

    def sync_record(self, node):
        node.save()
          
