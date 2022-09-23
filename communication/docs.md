# Communication structure and logic:
 1) Container side:
    * bash script that restores catkin ws and asks is it ok to remove
    * other script asks whether the repo should be synced(pushed)
 2) Backend side:
    * flask handlers which wait for request on a certain endpoints for saving or restoring the repo
    * here also example code to create and clone is available
> Prerequisites: flask, gitpython
---
## General logic:
1) User logs into the session and the **session token** is created and stored in the database
2) `check_project()` function in app.py checks whether the repo with the username specified exists and if doesn't creates one
3) Then repo can be cloned with example in `api_repo_clone()` of app.py and the container can be launched with mounted volume

> Optional step if the user wants to restore repo:
* Run script inside the container which uses token id from inside to contact the backend and function `api_repo_reclone()` that handles that request.
4) After session finishes or the user decides to save he does the same way as in the previous step but this time to contact `api_repo_commit_push()` .  However, if there are no changes made there's a check which will prevent empty commit.