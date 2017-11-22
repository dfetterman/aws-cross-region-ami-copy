# LambdaAMICopyAcrossRegion

�	This script will first search for the AMI created for the date specified in the source AWS region (Ex: Mumbai (ap-south-1)).

�	As soon as it loops the AMI, it checks for the same AMI already exists in the destination AWS region (Ex: Singapore (ap-southeast-1)). 

�	If the AMI doesn�t exist or already copied then it copies AMI to the destination region.

�	After copying the AMI it creates a "DeleteOnCopy" tag on the AMI-indicating when it will be deleted using the Retention value and another Lambda function.


# LambdaCleanupCopiedAMI

�	It checks and stores the every image that's reached its �DeleteOnCopy� tag's date for deletion.

�	It then loops through the AMIs, de-registers them and removes all the snapshots associated with those AMI.


# Important Note:
 Please specify your AWS Account Number in the place of "XXXXX" where ever in the code
