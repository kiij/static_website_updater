## static_website_updater

This is a configurable tool to dynamically update and publish static websites. For example, let's say you want your
Jekyll blog to have a post for each photo in a Flickr album of yours. You could manually create a post for each photo,
but that would be tedious. Instead, you could run this tool and it would automatically create a post for each photo in
your Flickr album, then publish the newly generated static site to your destination of choice. If you set this tool up
as a cron job, you could even have your blog pull in new photos from your Flickr album daily.

The tool performs the following process to make this happen:

1. Check out your Jekyll site scaffold from the git repository you specify.
2. Create posts in your Jekyll site scaffold for content that is gathered from the sources you configure (such as Flickr).
3. Commit the posts to the git repository for your Jekyll site scaffold.
4. Publish your updated Jekyll site as static HTML somewhere (such as S3).
5. Push the new commit back to git repository.

### Supported Functionality

The code is structured in a way that new content sources and new publishing methods can be added modularly as needed.

*Currently supported content sources*

- Flickr

*Currently supported publishing methods*

- Upload to S3

### Installation

Before you start, you'll need Ruby installed. You'll also need the `bundler`, `jekyll`, and `jekyll-paginate` Ruby gems installed.

After that, you can install and use this tool with the following commands:

    git checkout https://github.com/kiij/static_website_updater.git
    cd static_website_updater
    sudo python setup.py install
    static_website_updater my_config.json

#### Using Vagrant

This tool depends on Ruby and Python, both of which are infamous for making it difficult to get the right versions of
the language and the necessary dependencies installed correctly. If you're having problems following the instructions
in the previous section, I highly suggest just running everything in a virtual machine.

There's an included Vagrant configuration that you can use to do this:

    git checkout https://github.com/kiij/static_website_updater.git
    cd static_website_updater
    vagrant box add ubuntu/trusty32
    vagrant up
    vagrant ssh
    
    cd /vagrant
    sudo python setup.py install
    /usr/local/bin/static_website_updater my_config.json

### Usage

You need to tell the tool where to pull content from, as well as where to publish your final generated website. Also,
you'll need to tell it where your Jekyll site's git repository is. This is all done through a JSON configuration file.
For an example of the format, see `sample_configurations/sample.json`.

After you've created your own configuration file, just provide its filename as the argument when you run the tool:

    static_site_updater your_config_file.json

#### Remote deployment

If you want to set this tool up to run regularly, and you don't already have an always-on server where you can stick it
in as a cron job, you might want to do so using a cloud server provider. A cloud server would start up at your desired
frequency, run the command, then shut down and delete itself.

An example Packer configuration is included that generates a DigitalOcean snapshot for this purpose. Instances created
from this snapshot will run the tool at boot, reading the JSON configuration from the User Data of the instance. To have
this happen regularly, you need to set it up so a new instance is started up from the snapshot regularly at that
interval. You could do this using a service like AWS Lambda, where you can set up a scheduled job to call the
DigitalOcean API to start up a new instance from the saved snapshot. And don't forget to also destroy the instance once
it's booted and run the tool.

To create a snapshot:

    packer build -var 'digitalocean_api_token=your_token_here' packer/digitalocean.json