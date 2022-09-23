from git import Repo
import os
import shutil


def clone(link: str, token_name: str, token: str, root_path: str, force: bool = False) -> str:
    """Clones git repo

    Args:
        link (str): link to repo
        token_name (str): name of the token
        token (str): token itself
        root_path (str): root path to save directory(username directory will be created inside)
        force (bool): if folder exists should it be removed
    """
    

    # clone_link = 'https://t1:V6FgRAo8JkMiBhgT98Yc@gitlab.ut.ee/aleksandr.makarov/test.git'

    beginning = link[:link.find('gitlab')]
    end = link[link.find('gitlab'):]
    clone_link = f'{beginning}{token_name}:{token}@{end}'

    path = os.path.join(root_path, link.split('/')[-1].split('.')[0])

    if os.path.exists(path):
        if force: 
            shutil.rmtree(path)
            Repo.clone_from(clone_link, path)
        else:
            repo = Repo(path)
            o = repo.remotes.origin
            o.pull()
    else:
        Repo.clone_from(clone_link, path)
    return 'success'