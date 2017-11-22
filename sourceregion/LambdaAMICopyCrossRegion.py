#This script copies the AMI to other region where source ami is tagged "CrossAccntRepli" and tag copied AMI 'DeleteOn' with retention  days specified.
import boto3
import json
from dateutil import parser
import dateutil
import datetime
import collections

#Specify the source region of AMI's created and the destination region to which AMI's to be copied
source_region = 'us-east-1'
source_image_resource = boto3.resource('ec2',source_region)
dest_image_client = boto3.client('ec2','us-west-2')
dest_image_resource  = boto3.resource('ec2','us-west-2')

#AMI to be retained for the number of days in the destination region.
ami_retention = 15

def copy_latest_image():
    images = source_image_resource.images.filter(Owners=["XXXXX"]) # Specify your AWS account owner id in place of "XXXXX" at all the places in this script
    
    #Retention days in DR region, its for 15 days.
    retention_days = int(ami_retention)
	
    to_tag = collections.defaultdict(list)
    
    for image in images:
        if image.tags is not None: 
            for t in image.tags:
                if t['Key'] == 'CrossAccntRepli' and t.get('Value') is  not None:
        
                    #Copy todays images
                    image_date = parser.parse(image.creation_date)
                    if image_date.date() == (datetime.datetime.today()).date(): 
        
	                #To Copy previous day images
                    #if image_date.date() == (datetime.datetime.today()-datetime.timedelta(1)).date(): 
		            
                        if not dest_image_client.describe_images(Owners=['XXXXX',],Filters=[{'Name':'name','Values':[image.name]}])['Images']:
                        #if not dest_image_client.describe_images(Owners=['XXXXX',])['Images']:
            
                            print "Copying Image {name} - {id} to us-west-2".format(name=image.name,id=image.id)
                            new_ami = dest_image_client.copy_image(
                                DryRun=False,
                                SourceRegion=source_region,
                                SourceImageId=image.id,
                                Name=image.name,
                                Description=image.description
                            )
                
                            to_tag[retention_days].append(new_ami['ImageId'])
                
                            print "New Image Id {new_id} for us-east-1 Image {name} - {id}".format(new_id=new_ami,name=image.name,id=image.id)
                
                
                            print "Retaining AMI %s for %d days" % (
                                    new_ami['ImageId'],
                                    retention_days,
                                )
                    
                            for ami_retention_days in to_tag.keys():
                                delete_date = datetime.date.today() + datetime.timedelta(days=retention_days)
                                delete_fmt = delete_date.strftime('%m-%d-%Y')
                                print "Will delete %d AMIs on %s" % (len(to_tag[retention_days]), delete_fmt)
                    
                                #To create a tag to an AMI when it can be deleted after retention period expires
                                dest_image_client.create_tags(
                                    Resources=to_tag[retention_days],
                                    Tags=[
                                        {'Key': 'DeleteOn', 'Value': delete_fmt},
                                        ]
                                    )
            else:
                print "Image {name} - {id} already present in xxx Region or falls outside of date created scope".format(name=image.name,id=image.id)

def lambda_handler(event, context):
    copy_latest_image()


if __name__ == '__main__':
    lambda_handler(None, None)

