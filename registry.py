#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

routines for querying the registry

"""
from settings import *

REG_DEV='http://casx019-zone1.ast.cam.ac.uk/registry/services/RegistryQueryv1_0'
REG_REL='http://registry.vamdc.eu/registry-12.07/services/RegistryQueryv1_0'
# use registry defined in settings if defined
try:
  WSDL = REGURL + '?wsdl'
except:
  REGURL = REG_REL
  WSDL = REGURL+'?wsdl'

from suds.client import Client
from suds.xsd.doctor import Doctor

class RegistryDoctor(Doctor):
    TNS = 'http://www.ivoa.net/wsdl/RegistrySearch/v1.0'
    def examine(self, node):
        tns = node.get('targetNamespace')
        # find a specific schema
        if tns != self.TNS:
            return
        for e in node.getChildren('element'):
            # find our response element
            if e.get('name') != 'XQuerySearchResponse':
                continue
            # fix the <xs:any/> by adding maxOccurs
            any = e.childAtPath('complexType/sequence/any')
            any.set('maxOccurs', 'unbounded')
            break


def getNodeList():

    d = RegistryDoctor()
    client = Client(WSDL) #,doctor=d)

    qr="""declare namespace ri='http://www.ivoa.net/xml/RegistryInterface/v1.0';
<nodes>
{
   for $x in //ri:Resource
   where $x/capability[@standardID='ivo://vamdc/std/VAMDC-TAP']
   and $x/@status='active'
   and $x/capability[@standardID='ivo://vamdc/std/VAMDC-TAP']/versionOfStandards='12.07'
   return 
   <node><title>{$x/title/text()}</title>
   <url>{$x/capability[@standardID='ivo://vamdc/std/VAMDC-TAP']/interface/accessURL/text()}</url>
   <identifier>{$x/identifier/text()}</identifier>
   <maintainer>{$x/curation/contact/email/text()}</maintainer>
   </node>   
}
</nodes>"""


    v=client.service.XQuerySearch(qr)
    nameurls=[]
    for node in v.node:
        # take only the first url
        try:
            url = node.url.split(" ")[0]
        except:
            url = None
            
        try:
	    email = node.maintainer
	except:
	    email = "Email not set in the registry"
            
        nameurls.append({\
            'name':node.title,
            'url':url,
            'identifier':node.identifier,
            'maintainer':email
            })
    return nameurls



if __name__ == '__main__':
    print getNodeList()
