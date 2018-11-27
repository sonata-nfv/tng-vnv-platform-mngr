#!/usr/bin/python

from flask import Flask, request, jsonify, render_template
import os, sys, logging, uuid, json
from werkzeug import secure_filename

#import serviceplatform
import psycopg2
import requests
import subprocess
import models.database as database

FILE = "db-config.cfg"

  


class Adapter:

    def __init__(self, name):
        self.name = name
        self.host = "host"
        self.type = "type" 

    def getName(self):
        return self.name
    def setName(self, newName):
        self.name = newName        

    def getHost(self):
        return self.host
    def setHost(self, newHost):
        self.host = newHost

    def getType(self):
        return self.type
    def setType(self, newType):
        self.type = newType        


    def getDBType(self):
        try:
            db = database.Database(FILE)
            connection = psycopg2.connect(user = db.user,
                                        password = db.password,
                                        host = db.host,
                                        port = db.port,
                                        database = db.database)  
            cursor = connection.cursor()
            print ( connection.get_dsn_parameters(),"\n")
            #create table Service Platforms
            get_type = "SELECT type FROM service_platforms WHERE name=\'" +self.name+ "\'"
            print (get_type)
            cursor.execute(get_type)
            all = cursor.fetchall()
            #return jsonify(all), 200 
            type_0 = all.__str__()
            print(type_0)
            type_1 = type_0[3:]            
            print(type_1)            
            type_2 = type_1[:-4]            
            print(type_2)                  
            return type_2
        except (Exception, psycopg2.Error) as error :
            print (error)
            exception_message = str(error)
            return exception_message, 401
        finally:
            #closing database connection.
                if(connection):
                    cursor.close()
                    connection.close()
                    print("PostgreSQL connection is closed") 

    def getDBHost(self):
        try:
            db = database.Database(FILE)
            connection = psycopg2.connect(user = db.user,
                                        password = db.password,
                                        host = db.host,
                                        port = db.port,
                                        database = db.database)  
            cursor = connection.cursor()
            print ( connection.get_dsn_parameters(),"\n")
            #create table Service Platforms
            print (self.name)
            get_host = "SELECT host FROM service_platforms WHERE name=\'" +self.name+ "\'"
            print (get_host)
            cursor.execute(get_host)
            all = cursor.fetchall()
            #return jsonify(all), 200  
            return all, 200    
        except (Exception, psycopg2.Error) as error :
            print (error)
            exception_message = str(error)
            return exception_message, 401
        finally:
            #closing database connection.
                if(connection):
                    cursor.close()
                    connection.close()
                    print("PostgreSQL connection is closed") 


    def getPackages(self):    

        JSON_CONTENT_HEADER = {'Content-Type':'application/json'}   
        my_type =  self.getDBType()
        if my_type == 'sonata':               

            sp_host_0 = self.getDBHost()
            print (sp_host_0)
            sp_host = sp_host_0.__str__()
            print (sp_host)
            #print (self.getDBHost())
            sp_host_1 = sp_host[4:]
            print ("sp1 es: ")
            print (sp_host_1)
            sp_host_2 = sp_host_1[:-10]
            print ("sp2 es: ")
            print (sp_host_2)

            url = sp_host_2 + '/packages'
            #url = sp_url + '/packages'
            response = requests.get(url, headers=JSON_CONTENT_HEADER)    
            if response.ok:        
                    return (response.text, response.status_code, response.headers.items()) 
        if my_type == 'osm': 
            return "osm packages"



    def getPackage(self,name,vendor,version):    

        JSON_CONTENT_HEADER = {'Content-Type':'application/json'} 

        my_type =  self.getDBType()
        if my_type == 'sonata':    
            sp_host_0 = self.getDBHost()
            print (sp_host_0)
            sp_host = sp_host_0.__str__()
            print (sp_host)
            #print (self.getDBHost())
            sp_host_1 = sp_host[4:]
            print ("sp1 es: ")
            print (sp_host_1)
            sp_host_2 = sp_host_1[:-10]
            print ("sp2 es: ")
            print (sp_host_2)

            url = sp_host_2 + '/packages'  
            print (name,vendor,version)
            response = requests.get(url,headers=JSON_CONTENT_HEADER)
            response_json = response.content
            jjson = json.loads(response_json)
            pkg = [x for x in jjson if x['pd']['name'] == name and x['pd']['vendor'] == vendor and x['pd']['version'] == version]
            
            if response.ok: 
                    print(pkg)
                    return jsonify(pkg)

    def deletePackage(self,name,vendor,version):    

        JSON_CONTENT_HEADER = {'Content-Type':'application/json'}   

        my_type =  self.getDBType()
        if my_type == 'sonata':    
            sp_host_0 = self.getDBHost()
            print (sp_host_0)
            sp_host = sp_host_0.__str__()
            print (sp_host)
            #print (self.getDBHost())
            sp_host_1 = sp_host[4:]
            print ("sp1 es: ")
            print (sp_host_1)
            sp_host_2 = sp_host_1[:-10]
            print ("sp2 es: ")
            print (sp_host_2)

            url = sp_host_2 + '/packages'  
            print (name,vendor,version)
            response = requests.get(url,headers=JSON_CONTENT_HEADER)
            response_json = response.content
            jjson = json.loads(response_json)
            pkg = [x for x in jjson if x['pd']['name'] == name and x['pd']['vendor'] == vendor and x['pd']['version'] == version]
            
            if pkg:

                print(pkg)
                #uuid_to_delete = pkg['pd']['uuid']
                #uuid_to_delete_1 = [uuid for x in jjson if x['pd']['name'] == name and x['pd']['vendor'] == vendor and x['pd']['version'] == version]
                uuid_to_delete_1 = [obj['uuid'] for obj in jjson if(obj['pd']['name'] == name)]            
                print(uuid_to_delete_1)
                uuid_0 = uuid_to_delete_1.__str__()
                uuid_to_delete_2 = uuid_0[2:]
                print(uuid_to_delete_2)
                uuid_to_delete_3 = uuid_to_delete_2[:-2]
                print(uuid_to_delete_3)

                url_for_delete = url + '/' + uuid_to_delete_3
                print (url_for_delete)
                delete = requests.delete(url_for_delete, headers=JSON_CONTENT_HEADER)

            if response.ok:                 
                    return (delete.text, delete.status_code, delete.headers.items())




    def getPackagebyId(self,name,vendor,version):    

        JSON_CONTENT_HEADER = {'Content-Type':'application/json'} 
        
        my_type =  self.getDBType()
        if my_type == 'sonata':              

            sp_host_0 = self.getDBHost()
            print (sp_host_0)
            sp_host = sp_host_0.__str__()
            print (sp_host)
            #print (self.getDBHost())
            sp_host_1 = sp_host[4:]
            print ("sp1 es: ")
            print (sp_host_1)
            sp_host_2 = sp_host_1[:-10]
            print ("sp2 es: ")
            print (sp_host_2)

            url = sp_host_2 + '/packages'  
            print (name,vendor,version)
            response = requests.get(url,headers=JSON_CONTENT_HEADER)
            response_json = response.content
            jjson = json.loads(response_json)
            pkg = [x for x in jjson if x['pd']['name'] == name and x['pd']['vendor'] == vendor and x['pd']['version'] == version]
            
            if pkg:

                print(pkg)
                #uuid_to_delete = pkg['pd']['uuid']
                #uuid_to_delete_1 = [uuid for x in jjson if x['pd']['name'] == name and x['pd']['vendor'] == vendor and x['pd']['version'] == version]
                uuid_to_delete_1 = [obj['uuid'] for obj in jjson if(obj['pd']['name'] == name)]            
                print(uuid_to_delete_1)
                uuid_0 = uuid_to_delete_1.__str__()
                uuid_to_delete_2 = uuid_0[2:]
                print(uuid_to_delete_2)
                uuid_to_delete_3 = uuid_to_delete_2[:-2]
                print(uuid_to_delete_3)

                url_for_delete = url + '/' + uuid_to_delete_3
                print (url_for_delete)
                delete = requests.get(url_for_delete, headers=JSON_CONTENT_HEADER)

            if response.ok:                 
                    return (delete.text, delete.status_code, delete.headers.items())                

                

                



    def uploadPackage(self,package):

        JSON_CONTENT_HEADER = {'Content-Type':'application/json'}   
        my_type =  self.getDBType()
        if my_type == 'sonata':               

            sp_host_0 = self.getDBHost()
            print (sp_host_0)
            sp_host = sp_host_0.__str__()
            print (sp_host)
            #print (self.getDBHost())
            sp_host_1 = sp_host[4:]
            print ("sp1 es: ")
            print (sp_host_1)
            sp_host_2 = sp_host_1[:-10]
            print ("sp2 es: ")
            print (sp_host_2)
            url = sp_host_2 + '/packages'
            
            print(package)
            print(url)

            files = {'package': open(package,'rb')}
            upload = requests.post(url, files=files)

            if request.method == 'POST':
                return upload.text

    def uploadOSMService(self,service): 
        JSON_CONTENT_HEADER = {'Content-Type':'application/json'}   
        my_type =  self.getDBType()
        if my_type == 'osm':               

            sp_host_0 = self.getDBHost()
            print (sp_host_0)
            sp_host = sp_host_0.__str__()
            print (sp_host)
            #print (self.getDBHost())
            sp_host_1 = sp_host[4:]
            print ("sp1 es: ")
            print (sp_host_1)
            sp_host_2 = sp_host_1[:-10]
            print ("sp2 es: ")
            print (sp_host_2)

            sp_host_3 = sp_host_2[7:]
            print ("sp3 es: ")
            print (sp_host_3)            

            url = sp_host_2 + '/services'
            
            
            print(service)
            upload_nsd = "osm --hostname " + sp_host_3 + " nsd-create " + service
            print (upload_nsd)
            upload = subprocess.check_output([upload_nsd], shell=True)
            return (upload)
      

    def uploadOSMFunction(self,function): 
        JSON_CONTENT_HEADER = {'Content-Type':'application/json'}   
        my_type =  self.getDBType()
        if my_type == 'osm':               

            sp_host_0 = self.getDBHost()
            print (sp_host_0)
            sp_host = sp_host_0.__str__()
            print (sp_host)
            #print (self.getDBHost())
            sp_host_1 = sp_host[4:]
            print ("sp1 es: ")
            print (sp_host_1)
            sp_host_2 = sp_host_1[:-10]
            print ("sp2 es: ")
            print (sp_host_2)

            sp_host_3 = sp_host_2[7:]
            print ("sp3 es: ")
            print (sp_host_3)            

            url = sp_host_2 + '/functions'
            
            
            print(function)
            upload_vnfd = "osm --hostname " + sp_host_3 + " vnfd-create " + function
            print (upload_vnfd)
            upload = subprocess.check_output([upload_vnfd], shell=True)
            return (upload)      



    def getServices(self):    

        JSON_CONTENT_HEADER = {'Content-Type':'application/json'}  
        my_type =  self.getDBType()
        if my_type == 'sonata':                

            sp_host_0 = self.getDBHost()
            print (sp_host_0)
            sp_host = sp_host_0.__str__()
            print (sp_host)
            #print (self.getDBHost())
            sp_host_1 = sp_host[4:]
            print ("sp1 es: ")
            print (sp_host_1)
            sp_host_2 = sp_host_1[:-10]
            print ("sp2 es: ")
            print (sp_host_2)

            url = sp_host_2 + '/services'
            #url = sp_url + '/packages'
            response = requests.get(url, headers=JSON_CONTENT_HEADER)    
            if response.ok:        
                    return (response.text, response.status_code, response.headers.items()) 

        if my_type == 'osm':                

            sp_host_0 = self.getDBHost()
            print (sp_host_0)
            sp_host = sp_host_0.__str__()
            print (sp_host)
            sp_host_1 = sp_host[4:]
            print ("sp1 es: ")
            print (sp_host_1)
            sp_host_2 = sp_host_1[:-10]
            print ("sp2 es: ")
            print (sp_host_2)
            sp_host_3 = sp_host_2[7:]
            print ("sp3 es: ")
            print (sp_host_3)            

            url = sp_host_2 + '/services'
            get_nsd_list = "osm --hostname " + sp_host_3 + " nsd-list"
            print (get_nsd_list)
            #get = os.system(get_nsd_list).__str__()    
            #return get
            get = subprocess.check_output([get_nsd_list], shell=True)
            return (get)
            

    def getFunctions(self):    

        JSON_CONTENT_HEADER = {'Content-Type':'application/json'}  
        my_type =  self.getDBType()
        if my_type == 'sonata':                

            sp_host_0 = self.getDBHost()
            print (sp_host_0)
            sp_host = sp_host_0.__str__()
            print (sp_host)
            #print (self.getDBHost())
            sp_host_1 = sp_host[4:]
            print ("sp1 es: ")
            print (sp_host_1)
            sp_host_2 = sp_host_1[:-10]
            print ("sp2 es: ")
            print (sp_host_2)

            url = sp_host_2 + '/functions'
            #url = sp_url + '/packages'
            response = requests.get(url, headers=JSON_CONTENT_HEADER)    
            if response.ok:        
                    return (response.text, response.status_code, response.headers.items()) 

        if my_type == 'osm':                

            sp_host_0 = self.getDBHost()
            print (sp_host_0)
            sp_host = sp_host_0.__str__()
            print (sp_host)
            #print (self.getDBHost())
            sp_host_1 = sp_host[4:]
            print ("sp1 es: ")
            print (sp_host_1)
            sp_host_2 = sp_host_1[:-10]
            print ("sp2 es: ")
            print (sp_host_2)
            sp_host_3 = sp_host_2[7:]
            print ("sp3 es: ")
            print (sp_host_3)            

            url = sp_host_2 + '/functions'
            get_vnfd_list = "osm --hostname " + sp_host_3 + " vnfd-list"
            print (get_vnfd_list)
            #get = os.system(get_nsd_list).__str__()
            #return get                    
            get = subprocess.check_output([get_vnfd_list], shell=True)
            return (get)            

    def getService(self,name,vendor,version):    

        JSON_CONTENT_HEADER = {'Content-Type':'application/json'}  

        my_type =  self.getDBType()
        if my_type == 'sonata':                

            sp_host_0 = self.getDBHost()
            print (sp_host_0)
            sp_host = sp_host_0.__str__()
            print (sp_host)
            #print (self.getDBHost())
            sp_host_1 = sp_host[4:]
            print ("sp1 es: ")
            print (sp_host_1)
            sp_host_2 = sp_host_1[:-10]
            print ("sp2 es: ")
            print (sp_host_2)

            url = sp_host_2 + '/services'  
            print (name,vendor,version)
            response = requests.get(url,headers=JSON_CONTENT_HEADER)
            response_json = response.content
            jjson = json.loads(response_json)
            pkg = [x for x in jjson if x['nsd']['name'] == name and x['nsd']['vendor'] == vendor and x['nsd']['version'] == version]
            
            if response.ok: 
                    print(pkg)
                    return jsonify(pkg)     

    def getServiceInstantiations(self,name,vendor,version):    

        JSON_CONTENT_HEADER = {'Content-Type':'application/json'}  

        my_type =  self.getDBType()
        if my_type == 'sonata':                

            sp_host_0 = self.getDBHost()
            print (sp_host_0)
            sp_host = sp_host_0.__str__()
            print (sp_host)
            #print (self.getDBHost())
            sp_host_1 = sp_host[4:]
            print ("sp1 es: ")
            print (sp_host_1)
            sp_host_2 = sp_host_1[:-10]
            print ("sp2 es: ")
            print (sp_host_2)

            url = sp_host_2 + '/requests'  
            print (name,vendor,version)
            response = requests.get(url,headers=JSON_CONTENT_HEADER)
            response_json = response.content
            #response_json = response.text
            print (response_json)
            #json_str = json.dumps(response._content)
            #jjson = json.loads(response.text.__str__())
            #jjson = json.loads(response_json)
            jjson = json.loads(response.content)
            print (jjson)
            #services = [x for x in jjson if x['service']['name'] == name and x['service']['vendor'] == vendor and x['service']['version'] == version]

            #print (jjson['service']['name'])
            #print (obj for obj in jjson if(obj['service']['vendor'] == 'eu.5gtango'))
            #illo = [obj for obj in jjson if(obj['service'] == '11111')]
            
            print ("illo")
            #idd = print ([obj for obj in jjson[0]['service']['uuid']])
            idd = print (jjson[0]['service']['uuid'])
            idd = print (jjson[0]['service']['name'])
            idd = print (jjson[1]['service']['uuid'])
            idd = print (jjson[1]['service']['name'])            
   
            #idd = [obj.service['name'] for obj in jjson]
            print ("illo")
            
            
            N = 0
            for N in range(10000):
                print (jjson['service']['uuid'])

                N = N + 1
                print (N)


            

            


            if response.ok:        
                #return (response.text, response.status_code, response.headers.items())      
                    return jsonify("no")
                            


    def getServiceId(self,name,vendor,version):    

        JSON_CONTENT_HEADER = {'Content-Type':'application/json'}  
        my_type =  self.getDBType()
        if my_type == 'sonata':                

            sp_host_0 = self.getDBHost()
            print (sp_host_0)
            sp_host = sp_host_0.__str__()
            print (sp_host)
            #print (self.getDBHost())
            sp_host_1 = sp_host[4:]
            print ("sp1 es: ")
            print (sp_host_1)
            sp_host_2 = sp_host_1[:-10]
            print ("sp2 es: ")
            print (sp_host_2)

            url = sp_host_2 + '/services'  
            print (name,vendor,version)
            response = requests.get(url,headers=JSON_CONTENT_HEADER)
            response_json = response.content
            print (response_json)
            jjson = json.loads(response_json)
            pkg = [x for x in jjson if x['nsd']['name'] == name and x['nsd']['vendor'] == vendor and x['nsd']['version'] == version]
            
            if pkg:

                print(pkg)
                uuid_to_delete_1 = [obj['uuid'] for obj in jjson if(obj['nsd']['name'] == name)]            
                print(uuid_to_delete_1)
                uuid_0 = uuid_to_delete_1.__str__()
                uuid_to_delete_2 = uuid_0[2:]
                print(uuid_to_delete_2)
                uuid_to_delete_3 = uuid_to_delete_2[:-2]
                print(uuid_to_delete_3)
                url_for_delete = url + '/' + uuid_to_delete_3
                print (url_for_delete)
                delete = requests.get(url_for_delete, headers=JSON_CONTENT_HEADER)
        
            if response.ok:                                        
                    return uuid_to_delete_3


    def instantiationStatus(self,id):    

        JSON_CONTENT_HEADER = {'Content-Type':'application/json'}   
        my_type =  self.getDBType()

        if my_type == 'sonata':
            print('this SP is a Sonata')
            sp_host_0 = self.getDBHost()
            print (sp_host_0)
            sp_host = sp_host_0.__str__()
            print (sp_host)
            #print (self.getDBHost())
            sp_host_1 = sp_host[4:]
            print ("sp1 es: ")
            print (sp_host_1)
            sp_host_2 = sp_host_1[:-10]
            print ("sp2 es: ")
            print (sp_host_2)

            url = sp_host_2 + '/requests/' +  id
            print (url)
            
            response = requests.get(url,headers=JSON_CONTENT_HEADER)
            response_json = response.content
            print (response_json)
            #return response_json
            if response.ok:        
                return (response.text, response.status_code, response.headers.items()) 


        if my_type == 'osm':
            print('this SP is a OSM')   
            print('this SP is a OSM')
            sp_host_0 = self.getDBHost()
            print (sp_host_0)
            sp_host = sp_host_0.__str__()
            print (sp_host)
            sp_host_1 = sp_host[4:]
            print ("sp1 es: ")
            print (sp_host_1)
            sp_host_2 = sp_host_1[:-10]
            print ("sp2 es: ")
            print (sp_host_2)
            sp_host_3 = sp_host_2[7:]
            print ("sp3 es: ")
            print (sp_host_3)            
            url = sp_host_3            
            
            get_status = "osm --hostname " + sp_host_3 + " ns-op-list " + id
            print (get_status)
            status = subprocess.check_output([get_status], shell=True)
            return (status)              


    def instantiationsStatus(self):    

        JSON_CONTENT_HEADER = {'Content-Type':'application/json'}   
        my_type =  self.getDBType()

        if my_type == 'sonata':
            print('this SP is a Sonata')
            sp_host_0 = self.getDBHost()
            print (sp_host_0)
            sp_host = sp_host_0.__str__()
            print (sp_host)
            #print (self.getDBHost())
            sp_host_1 = sp_host[4:]
            print ("sp1 es: ")
            print (sp_host_1)
            sp_host_2 = sp_host_1[:-10]
            print ("sp2 es: ")
            print (sp_host_2)

            url = sp_host_2 + '/requests'  
            print (url)
            
            response = requests.get(url,headers=JSON_CONTENT_HEADER)
            response_json = response.content
            print (response_json)
            #return response_json
            if response.ok:        
                return (response.text, response.status_code, response.headers.items())

            #print("status")
            #return "status"
        if my_type == 'osm':
            print('this SP is a OSM')
            sp_host_0 = self.getDBHost()
            print (sp_host_0)
            sp_host = sp_host_0.__str__()
            print (sp_host)
            sp_host_1 = sp_host[4:]
            print ("sp1 es: ")
            print (sp_host_1)
            sp_host_2 = sp_host_1[:-10]
            print ("sp2 es: ")
            print (sp_host_2)
            sp_host_3 = sp_host_2[7:]
            print ("sp3 es: ")
            print (sp_host_3)            
            url = sp_host_3            
            
            get_status = "osm --hostname " + sp_host_3 + " ns-list"
            print (get_status)
            status = subprocess.check_output([get_status], shell=True)
            return (status)              


    def instantiation(self,request):    

        JSON_CONTENT_HEADER = {'Content-Type':'application/json'}   
        my_type =  self.getDBType()

        if my_type == 'sonata':
            print('this SP is a Sonata')
            sp_host_0 = self.getDBHost()
            print (sp_host_0)
            sp_host = sp_host_0.__str__()
            print (sp_host)
            #print (self.getDBHost())
            sp_host_1 = sp_host[4:]
            print ("sp1 es: ")
            print (sp_host_1)
            sp_host_2 = sp_host_1[:-10]
            print ("sp2 es: ")
            print (sp_host_2)
            url = sp_host_2 + '/requests'
            
            print(request.get_json())
            data = request.get_json()
            print(url)
            #upload = requests.post(url, files=files)
            
            #upload = requests.post(url, files=files)
            instantiate = requests.post(url,data,headers=JSON_CONTENT_HEADER) 

            if request.method == 'POST':
                return instantiate.text

        if my_type == 'osm':
            print('this SP is a OSM')  

            sp_host_0 = self.getDBHost()
            print (sp_host_0)
            sp_host = sp_host_0.__str__()
            print (sp_host)
            #print (self.getDBHost())
            sp_host_1 = sp_host[4:]
            print ("sp1 es: ")
            print (sp_host_1)
            sp_host_2 = sp_host_1[:-10]
            print ("sp2 es: ")
            print (sp_host_2)

            sp_host_3 = sp_host_2[7:]
            print ("sp3 es: ")
            print (sp_host_3)            

            url = sp_host_3
            print(request.get_json())
            data = request.get_json()
            print(url)
            print (data)
            print (data['nsd_name'])
            print (data['ns_name'])
            print (data['vim_account'])
            
            
            instantiate_nsd = "osm --hostname " + sp_host_3 + " ns-create --nsd_name " + data['nsd_name'] + " --ns_name " + data['ns_name']+ " --vim_account " + data['vim_account'] 
            print (instantiate_nsd)
            upload = subprocess.check_output([instantiate_nsd], shell=True)
            return (upload)             




    def instantiationDelete(self,request):    

        JSON_CONTENT_HEADER = {'Content-Type':'application/json'}   
        my_type =  self.getDBType()

        if my_type == 'sonata':
            print('this SP is a Sonata')

            print('this SP is a Sonata')
            sp_host_0 = self.getDBHost()
            print (sp_host_0)
            sp_host = sp_host_0.__str__()
            print (sp_host)
            #print (self.getDBHost())
            sp_host_1 = sp_host[4:]
            print ("sp1 es: ")
            print (sp_host_1)
            sp_host_2 = sp_host_1[:-10]
            print ("sp2 es: ")
            print (sp_host_2)
            url = sp_host_2 + '/requests'
            
            print(request.get_json())
            data = request.get_json()
            print(url)
            #upload = requests.post(url, files=files)
            
            #upload = requests.post(url, files=files)
            terminate = requests.post(url,data,headers=JSON_CONTENT_HEADER) 

            if request.method == 'POST':
                return terminate.text

        if my_type == 'osm':
            print('this SP is a OSM')  

            sp_host_0 = self.getDBHost()
            print (sp_host_0)
            sp_host = sp_host_0.__str__()
            print (sp_host)
            #print (self.getDBHost())
            sp_host_1 = sp_host[4:]
            print ("sp1 es: ")
            print (sp_host_1)
            sp_host_2 = sp_host_1[:-10]
            print ("sp2 es: ")
            print (sp_host_2)

            sp_host_3 = sp_host_2[7:]
            print ("sp3 es: ")
            print (sp_host_3)            

            url = sp_host_3
            print(request.get_json())
            data = request.get_json()
            print(url)
            print (data)
            #print (data['nsd_name'])
            print (data['ns_name'])
            
            
            
            delete_ns = "osm --hostname " + sp_host_3 + " ns-delete " + data['ns_name']
            print (delete_ns)
            delete = subprocess.check_output([delete_ns], shell=True)
            return (delete)                            


    def getOSMToken(self):            
        #JSON_CONTENT_HEADER = {'Content-Type':'application/json'}   
        JSON_CONTENT_HEADER = {'Accept':'application/yaml'}   
        my_type =  self.getDBType()

        if my_type == 'osm':
            print('this SP is a OSM')

            sp_host_0 = self.getDBHost()
            print (sp_host_0)
            sp_host = sp_host_0.__str__()
            print (sp_host)
            #print (self.getDBHost())
            sp_host_1 = sp_host[4:]
            print ("sp1 es: ")
            print (sp_host_1)
            sp_host_2 = sp_host_1[:-10]
            print ("sp2 es: ")
            print (sp_host_2)
            #url = sp_host_2 + '/requests'
            url = sp_host_2 + ':9999/osm/admin/v1/tokens'
            print (url)
            
            admin_data = "{username: 'admin', password: 'admin', project_id: 'admin'}"
            print (admin_data)

            get_token = requests.post(url,data=admin_data,headers=JSON_CONTENT_HEADER)
            print (get_token.text)

            return url
            #upload = requests.post(url, files=files)
            
            #upload = requests.post(url, files=files)
             
   