import os
import requests
import sels8s

serverless = sels8s.client.Serverless()


def deploy(*args, **kwargs):
    # Download updated package from GitHub public repo
    # NOTE(starodubcevna): For public repos simple git clone blah-blah-blah
    # will work fine. For private repos it's better to path developer token
    # rather than usernam:password or ssh key, e.g.
    # git clone https://<my_token>:x-oauth-basic@github.com/<user>/<repo>
    action_name = os.environ.get("ACTION_NAME")
    token = os.environ.get("DEPLOY_TOKEN")
    repo = os.environ.get("REPO_URL")
    branch = os.environ.get("BRANCH") or "master"
    constructed_url = f"https://{repo}/archive/{branch}.zip"

    print(f"constructed_url: {constructed_url}")
    if token:
        headers = {"Authorization": f"token {token}"}
        resp = requests.get(constructed_url, headers=headers)
    else:
        resp = requests.get(constructed_url)
    redirected_url = ''
    if resp.status_code == 200:
        redirected_url = resp.url
    else:
        print(f"Request to your repo failed with {resp.status_code}")
    rresp = requests.get(redirected_url, stream=True)
    if rresp.status_code == 200:
        with open("code_sample.zip", "wb") as f:
            for chunk in rresp:
                f.write(chunk)
    else:
        print(f"Request redirect o your repo failed with {rresp.status_code}")


    # Upload zip to Selectel Functions
    upload_resp = serverless.upload_module("code_sample.zip")
    if upload_resp.status_code == 200:
        print("New code upload successfully")
    else:
        print(f"Code upload failed with {upload_resp.status_code}")
        return
    # Get module_id from upload_resp
    module_id = upload_resp.json()["function_id"]
    # Update existing action with the new code
    edit_resp = serverless.edit_function(action_name, function_id=module_id)
    if edit_resp.status_code == 200:
        print("Function update")
    else:
        print(f"Function update failed with {edit_resp.status_code}")
        return
    # # Make test invoke and return activation id
    # invoke_resp = ss_client.invoke_function(action_name)
    # return invoke_resp["activationId"]
