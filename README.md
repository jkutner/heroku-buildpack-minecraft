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
