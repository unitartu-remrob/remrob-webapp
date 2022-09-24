from git import Repo 
import uuid

# TODO: check whether repo exists
def commit_push(path: str) -> str:
    """THis function does git add and if something changed commits and pushes the repository

    Args:
        path (str): path to the repo

    Returns:
        str: status
    """

    repo = Repo(path)
    repo.git.add(all=True)


    if repo.head.commit.diff(): 
        repo.index.commit(uuid.uuid4().hex[:8])
        origin = repo.remote(name="origin")
        origin.push()
        return 'success'
    else:
        return 'error: no changes detected'


