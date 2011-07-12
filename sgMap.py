#!/usr/bin/env python

import boto
import httplib

# this doesn't work
if boto.Version < 2:
    print "wrong boto version"
    exit()

# pseudoDNS users credentials
AccessKeyID = ""
secretAccessKey = ""

conn = boto.connect_ec2(AccessKeyID, secretAccessKey)

rules = {}

for region_local in [ conn.get_all_regions()[2] ]:
    print(region_local)
    conn_local = region_local.connect(aws_secret_access_key=secretAccessKey, aws_access_key_id=AccessKeyID)
    for sg in conn_local.get_all_security_groups():
        for rule in sg.rules:
            #rule.to_port to rule.from_port
            incoming = rule.grants[0]
            if incoming.name: print '"' + str(incoming.name) + '"',
            if incoming.cidr_ip: print '"' + incoming.cidr_ip + '"',
            print "->",
            print '"' + str(rule.parent.name) + '"',
            if rule.from_port == rule.to_port:
                print '[ label="' + str(rule.from_port) + '" ]',
            else:
                print '[ label="' + str(rule.from_port) + '-' + str(rule.to_port) + '" ]',
            print ";"
            #print incoming.name + incoming.cidr_ip + " " + str(rule.parent.name)

