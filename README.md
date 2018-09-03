## S3_Site_Maker
- [About](#about)
- [Installation and Configuration](#installation-and-configuration)
  - [Running the Initial Setup / Settings](#running-the-initial-setup--settings)
- [Basic Usage](#basic-usage)
  - [Initial Deployments](#initial-deployments)
  
## About

**S3_Site_Maker** let's you easily deploy a static webpace into an AWS S3 Bucket.
 S3 Buckets already make it easy to deploy a static site, but with this tool you are able
 to deploy and update your site directly from your command line with a few simple commands.
 
If you already have a static site setup, it's as easy as running the following commands from your project directory:

```
$ pip install s3_site_maker
$ s3_site_maker init
$ s3_site_maker deploy
```

## Installation and Configuration

_Before you begin, make sure you are running Python 3.7 and you have a valid AWS account and your 
[AWS credentials file](https://blogs.aws.amazon.com/security/post/Tx3D6U6WSFGOK2H/A-New-and-Standardized-Way-to-Manage-Credentials-in-the-AWS-SDKs) 
is properly installed._

**S3_Site_Maker** can easily be installed through pip:

    $ pip install s3_site_maker

**Note**: **S3_Site_Maker** can be installed globally but it's preferred that it be installed into your projects
virtual environment.

Next, you'll need to configure the settings.

### Initial Setup / Settings

**S3_Site_Maker** can automatically set up your deployment settings for your dev environment with the `init` command:

    $ s3_site_maker init

This command will create the **aws_site_maker.json** file, and let you configure the basic deployment settings. Which will look like the syntax below:

```javascript
{
    // The name of your environment
    "dev": {
        // The name of the S3 bucket where the site will be deployed to for this environment 
        "s3_bucket": "personalsite",
        "endpoints": {
            "index": "index.html",
            "error": "error.html"
        }
        "ignore" : []
    }
}
```
_Since an S3 bucket name can be used as a URL the chosen name needs to be globally unique and
must conform to the [AWS naming requirements](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-s3-bucket-naming-requirements.html)_

_If the bucket name does not adhere to the naming requirements, or it already exist and you don't
own it, then you will receive and error message during deployment. You will need to change the bucket
name manually in the aws_site_maker.json file._

You will also be asked to provide the names of the index and error files, which S3 static sites consist of. 
By default it assumes the names are "**index.html**" and "**error.html**". With the error page being shown when there
is an error for whatever reason. The files that are specified need to exist in the same directory as the **aws_site_maker.json**
file.

The configuration file also specifies an **"ignore"** field which can be used to list any files or folders that should 
not be uploaded to the S3 bucket. Everything not specified in this list will be uploaded by default.

You can define as many stages as you like - we recommend having _dev_, _staging_, and _production_.

Now, you're ready to deploy!

## Basic Usage

### Initial Deployments

At the moment 

Once your settings are configured, you can package and deploy your application to a stage called "dev" with a single command:

    $ s3_site_maker deploy dev
    Creating the bucket personalsite...
    Uploading file index.html...
    Uploading file error.html...
    Setting the bucket personalsite as a website...
    The website address is https://personalsite.s3-website-us-east-1.amazonaws.com

And now your site is available to everyone.

### Undeploy
You can also delete the content in the S3 bucket. Effectively dropping the site.This is done by running the command:

    $ s3_site_maker undeploy dev
    
The argument after the **undeploy** command is the name of the environment you want to drop.

