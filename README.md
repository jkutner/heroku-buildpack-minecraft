# Heroku Minecraft Buildpack

This is a [Heroku Buildpack](https://devcenter.heroku.com/articles/buildpacks)
for running a Minecraft server in a [dyno](https://devcenter.heroku.com/articles/dynos).

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## Usage

Create a [free ngrok account](https://ngrok.com/) and copy your Auth token. Then create a new Git project with a `eula.txt` file:

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
$ heroku buildpacks:add heroku/jvm
$ heroku buildpacks:add https://github.com/jkutner/heroku-buildpack-minecraft
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
Server available at: 0.tcp.ngrok.io:17003
```

Copy the `0.tcp.ngrok.io:17003` part, and paste it into your local Minecraft app
as the server name.

## Syncing to S3

The Heroku filesystem is [ephemeral](https://devcenter.heroku.com/articles/dynos#ephemeral-filesystem),
which means files written to the file system will be destroyed when the server is restarted.

Minecraft keeps all of the data for the server in flat files on the file system.
Thus, if you want to keep you world, you'll need to sync it to S3.

First, create an [AWS account](https://aws.amazon.com/) and an S3 bucket. Then configure the bucket
and your AWS keys like this:

```
$ heroku config:set AWS_BUCKET=your-bucket-name
$ heroku config:set AWS_ACCESS_KEY=xxx
$ heroku config:set AWS_SECRET_KEY=xxx
```

The buildpack will sync your world to the bucket every 60 seconds, but this is configurable by setting the `AWS_SYNC_INTERVAL` config var.

## Connecting to the server console

The Minecraft server runs inside a `screen` session. You can use [Heroku Exec](https://devcenter.heroku.com/articles/heroku-exec) to connect to your server console.

Once you have Heroku Exec installed, you can connect to the console using 

```
$ heroku ps:exec
Establishing credentials... done
Connecting to web.1 on ⬢ lovely-minecraft-2351...
$ screen -r minecraft
```

**WARNING** You are now connected to the Minecraft server. Use `Ctrl-A Ctrl-D` to exit the screen session. 
(If you hit `Ctrl-C` while in the session, you'll terminate the Minecraft server.)

## Customizing

### ngrok

You can customize ngrok by setting the `NGROK_OPTS` config variable. For example:

```
$ heroku config:set NGROK_OPTS="--remote-addr 1.tcp.ngrok.io:25565"
```

### Minecraft

You can choose the Minecraft version by setting the MINECRAFT_VERSION like so:

```
$ heroku config:set MINECRAFT_VERSION="1.8.3"
```

You can also configure the server properties by creating a `server.properties`
file in your project and adding it to Git. This is how you would set things like
Creative mode and Hardcore difficulty. The various options available are
described on the [Minecraft Wiki](http://minecraft.gamepedia.com/Server.properties).

You can add files such as `banned-players.json`, `banned-ips.json`, `ops.json`,
`whitelist.json` to your Git repository and the Minecraft server will pick them up.
