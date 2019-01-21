import json
import socket
import boto3
import hashlib
import copy
import urllib2

# ID of the security group we want to update
SECURITY_GROUP_ID = "sg-ID"

# DDNS Domain to update IP from
DDNS_DOMAIN = "my.DDNS.domain"

# Description of the security rule(s) we want to replace
SECURITY_RULE_DESCR = "DDNS_Update"


def lambda_handler(event, context):
    new_ip_address = socket.gethostbyname(DDNS_DOMAIN)
    result = update_security_group(new_ip_address)
    return result

    
def update_security_group(new_ip_address):
    new_cidr_ip="%s/32" % new_ip_address
    client = boto3.client('ec2')
    response = client.describe_security_groups(GroupIds=[SECURITY_GROUP_ID])
    group = response['SecurityGroups'][0]
    for permission in group['IpPermissions']:
        new_permission = copy.deepcopy(permission)
        ip_ranges = new_permission['IpRanges']
        permissions_changed=False
        for ip_range in ip_ranges:
            if 'Description' in ip_range:
                if ip_range['Description'] == SECURITY_RULE_DESCR:
                    if ip_range['CidrIp'] != new_cidr_ip:
                        ip_range['CidrIp'] = new_cidr_ip
                        permissions_changed = True
                        print(ip_range)
        if (permissions_changed == True):
            client.revoke_security_group_ingress(GroupId=group['GroupId'], IpPermissions=[permission])
            client.authorize_security_group_ingress(GroupId=group['GroupId'], IpPermissions=[new_permission])
        
    return new_cidr_ip if permissions_changed == True else  "No changes" 
