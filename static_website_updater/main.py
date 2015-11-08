#!/usr/bin/env python
import argparse
import sys

from static_website_updater.config.read_config import read_config_from_file, create_content_providers_from_config, create_git_from_config, create_publishers_from_config
from static_website_updater.website.jekyll_website import JekyllWebsite


def do(git, jekyll_website, content_providers, publishers):
    # Retrieve website from git
    print "Cloning from git"
    git.clone()

    # Cleanup the git repository of any old content
    print "Cleaning up"
    for content_provider in content_providers:
        content_provider.cleanup(jekyll_website)

    # Add the content
    print "Adding content"
    modified_files = set()
    for content_provider in content_providers:
        modified_files |= content_provider.add_content(jekyll_website)

    if not modified_files:
        print "No changed files detected, aborting"
        return

    # Commit the changed content
    print "Committing"
    commit_result = git.commit_files(modified_files, "Automatic update")

    if not commit_result:
        print "No diff in git detected, aborting"
        return

    # Build the website
    print "Building"
    jekyll_website.build()

    # Publish the built website
    print "Publishing"
    for publisher in publishers:
        publisher.publish(jekyll_website)

    # Push the content to git
    print "Pushing to git"
    git.push()

    # Exit
    print "Done"


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("config_file")

    args = parser.parse_args()

    # Read configuration
    config = read_config_from_file(args.config_file)
    git = create_git_from_config(config)
    jekyll_website = JekyllWebsite(git=git)
    content_providers = create_content_providers_from_config(config)
    publishers = create_publishers_from_config(config)

    do(git=git, jekyll_website=jekyll_website, content_providers=content_providers, publishers=publishers)

if __name__ == '__main__':
    sys.exit(main())
