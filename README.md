## S3-Site-Maker

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [About](#about)
- [Installation and Configuration](#installation-and-configuration)
  - [Running the Initial Setup / Settings](#running-the-initial-setup--settings)
- [Basic Usage](#basic-usage)
  - [Initial Deployments](#initial-deployments)
  <!-- END doctoc generated TOC please keep comment here to allow auto update -->
  
  
## About

**S3-Site-Maker** let's you easily deploy a static webpace into an AWS S3 Bucket.
 S3 Buckets already make it easy to deploy a static site, but with this tool you are able
 to deploy and update your site directly from your command line with a few simple commands.
 
If you've got a Python web app (including Django and Flask apps), it's as easy as:

```
$ pip install s3-site-maker
$ s3-site-maker init
$ s3-site-maker deploy
```

## Installation and Configuration

_Before you begin, make sure you are running Python 3.6 and you have a valid AWS account and your [AWS credentials file](https://blogs.aws.amazon.com/security/post/Tx3D6U6WSFGOK2H/A-New-and-Standardized-Way-to-Manage-Credentials-in-the-AWS-SDKs) is properly installed._

**S3-Site-Maker** can easily be installed through pip:

    $ pip install s3_site_maker

Please note that Zappa _**must**_ be installed into your project's [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

Next, you'll need to configure the settings.

### Initial Setup / Settings

**Zappa** can automatically set up your deployment settings for you with the `init` command:

    $ s3-site-maker init

This command will let you configure the basic deployment settings. By creating a json file named
aws_site_maker.json. Which will look like the syntax below:

```javascript
{
    // The name of your environment
    "dev": {
        // The name of the S3 bucket where the site will be deployed to for this environment 
        "s3_bucket": "personalsite",
    }
}
```

You can define as many stages as your like - we recommend having _dev_, _staging_, and _production_.

Now, you're ready to deploy!

## Basic Usage

### Initial Deployments

Once your settings are configured, you can package and deploy your application to a stage called "production" with a single command:

    $ s3_site_maker deploy dev
    Deploying..
    Your application is now live at: https://7k6anj0k99.execute-api.us-east-1.amazonaws.com/production

And now your app is **live!** How cool is that?!
