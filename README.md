# Heroku Minecraft Buildpack

This is a [Heroku Buildpack](https://devcenter.heroku.com/articles/buildpacks)
for running a Minecraft server in a [dyno](https://devcenter.heroku.com/articles/dynos).

## Usage

First, create an [ngrok](https://ngrok.com/) account and copy your Auth token.

Next, create a new Git project with a `eula.txt`:

```sh-session
$ echo 'eula=true' > eula.txt
$ git init
$ git add eula.txt
$ git commit -m "first commit"
```

Then, install the [Heroku toolbelt](https://toolbelt.heroku.com/).
Create a Heroku app, set your ngrok token, and push:

```sh-session
$ heroku create
$ heroku config:set NGROK_API_TOKEN="xxxxx"
$ git push heroku master
```

Finally, open the app:

```sh-session
$ heroku open
```

This will display the ngrok logs, which will contain the name of the server
(really it's a proxy, but whatever):

```
[03/11/15 02:06:21] [INFO] [client] Tunnel established at tcp://ngrok.com:45010
```

Copy the `ngrok.com:45010` part, and paste it into your local Minecraft app
as the server name.

## Syncing to S3

The Heroku filesystem is [ephemeral](https://devcenter.heroku.com/articles/dynos#ephemeral-filesystem),
which means files writen to the file system will be destroyed when the server is restarted.

Minecraft keeps all of the data for the server in flat files on the file system.
Thus, if you want to keep you world, you'll need to sync it to S3.

First, create an [AWS account] and an S3 bucket. Then configure the bucket
and your AWS keys like this:

```
$ heroku config:set AWS_BUCKET=your-bucket-name
$ heroku config:set AWS_ACCESS_KEY=xxx
$ heroku config:set AWS_SECRET_KEY=xxx
```

The buildpack will sync your world to the bucket every 5 seconds.

## Customizing

### ngrok

You can customize ngrok by setting the `NGROK_OPTS` config variable. For example:

```
$ heroku config:set NGROK_OPTS="-subdomain=my-subdomain"
```
