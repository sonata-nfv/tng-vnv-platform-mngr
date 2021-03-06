# VNF and Service Onboarding Walkthrough Using ONAP APIs

See powerpoint deck 'ONAP-API-Tutorial-for-5GTANGO.pptx' for details on running APIs.

## Using Postman

That repository contains 9 Postman collections and 2 environment files.
They have been tested with ONAP Casablanca.
You first need to import all those files into your Postman.
Each collection is made of several API operations.


Running all those collections, in the order, from 1 to 8 will create a lot of
objects in ONAP components :

- SDC : vendor, VSP, zip file upload, VF from VSP, Service, add VF to Service
- VID : OwningEntity, LineOfBusiness, Project, Platform
- AAI : customer, subscription, cloud region, tenant
- NBI : serviceOrder to add a service instance, serviceOrder to delete a service
 instance

The order is very important because a lot of API request will need the API
 response from the previous operation.

It is possible to run the complete collection using Postman.

You need, a zip file that contains Heat files for a VNF.

Collection 3 is about uploading that file into ONAP SDC.

Before running those collections, once in Postman, you need to have a look
at "globals" environment parameters.

All variables that begin by "auto_" must not be change (they will be modified
 using API response)
All other variables must be adapted to your needs.
In particular, you need to put your own values for cloud_region_id, tenant_name
 and tenant_id to fit with the place where you will instantiate the VNF

```yaml
 service:cirros
 vf_name:integration_test_VF_cirros
 vsp_name:integration_test_VSP
 vendor_name:onap_integration_vendor
 owning_entity:integration_test_OE
 platform:integration_test_platform
 project:integration_test_project
 lineofbusiness:integration_test_LOB
 customer_name:generic
 cloud_owner_name:OPNFV
 cloud_region_id:RegionOne
 tenant_name:openlab-vnfs
 tenant_id:234a9a2dc4b643be9812915b214cdbbb
 externalId:integration_test_BSS-001
 service_instance_name:integration_test_cirros_instance_001
 listener_url:http://10.4.2.65:8080/externalapi/listener/v1/listener
```

