from git import Repo
import os
import shutil

def clone(
        repo_url: str,
        token_name: str,
        token: str,
        repo_root_path: str,
        force: bool = False
    ) -> str:

    """Clones git repo

    Args:
        repo_url (str): link to repo
        token_name (str): name of the token
        token (str): token itself
        repo_root_path (str): root path to save directory(username directory will be created inside)
        force (bool): if folder exists should it be removed
    """

    # clone_link = 'https://t1:V6FgRAo8JkMiBhgT98Yc@gitlab.ut.ee/aleksandr.makarov/test.git'

    # Insert the token in the URL:
    beginning = repo_url[:repo_url.find('gitlab')]
    end = repo_url[repo_url.find('gitlab'):]
    clone_link = f'{beginning}{token_name}:{token}@{end}'

    # Create the path to the repo on the server
    # Extracts the name of the repo from the URL (without .git), so that the folder name is the same as the repo name
    path = os.path.join(repo_root_path, repo_url.split('/')[-1].split('.')[0])

    # Check if the user repo has already been created, if yes, pull the changes, if not, clone the repo
    # the "force" flag will force a reclone even if the folder exists

    if os.path.exists(path):
        if force:
            # Delete the folder (equivalent of rm -r) and clone again
            shutil.rmtree(path)
            Repo.clone_from(clone_link, path)
        else:
            repo = Repo(path)
            o = repo.remotes.origin
            o.pull()
    else:
        Repo.clone_from(clone_link, path)
        
    return 'success'