Selectel Serveless auto-deploy example
======================================

Introduction
------------

Here is an example of a function which can handle Github events and redeploy
another function deployed to Selectel Serverless

How to use
----------

Upload existing code to your project. You need to specify deploy_function/deploy
as file and module for your code, and deploy as function to be executed.

Don't forget environment variables for your function to be deployed:

ACTION_NAME=<name of a function to be edited>

DEPLOY_TOKEN=<deploy token if your repo is private, don't use if it's public>

REPO_URL=<github.com/{username}/{repo}

BRANCH=<branch_to_be_fetched>


Other variables can be imported from rc.sh
