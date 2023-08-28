from git import Repo 
import uuid

# TODO: check whether repo exists
def commit_push(path: str) -> str:
    """This function does git add and if something changed commits and pushes the repository with a random commit message

    Args:
        path (str): Path to the Git repository.

    Returns:
        str: status
    """

    repo = Repo(path)

    # repo.head.commit.diff() only considers changes that are part of the staging area. Untracked files are not included in this comparison, which is why we add everything before comparing
    repo.git.add(all=True)

    if repo.head.commit.diff(): 
        repo.index.commit(uuid.uuid4().hex[:8])
        origin = repo.remote(name="origin")
        origin.push()
        return 'success'
    else:
        return 'error: no changes detected'


