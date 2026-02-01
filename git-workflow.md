# Git workflow for working with source code

## Clone the git repository

This is a one-time step. The following command creates a new
directory `fastapi-course-freecodecamp` in the current directory. We will refer to the
`fastapi-course-freecodecamp` directory as your workspace.

```bash
git clone https://github.com/lokhandeganesh/fastapi-course-freecodecamp.git
cd fastapi-course-freecodecamp
```

The `clone` command populates your workspace with a copy of the remote
repository on gitlab.com. Every team member working on this
repository has such a copy of the remote repository in their
workspace. Everyone can commit changes to the code in their workspace
at will. The remote repository is unaffected by changes in local
workspaces. The commits from your workspace need to be pushed to
remote repository with `git push` command. The workflow for
committing code changes in your workspace and pushing them to remote
repository is outlined in the following sections.

By default, the `main` branch is checked out in your workspace.
Inspect the commit log from the main branch.

```bash
# See the current branch
git branch
# Inspect commit log, with latest commit at the top
git log
```

## Make code changes

Define the code change to be made, preferably in the form of a GitLab
issue. Scope of the code change should be clearly defined.
E.g. implementing a new HTTP route in flask Python app to return
completed DBT applications in JSON format.

### Step 1: start by pulling the latest from remote

The following command brings your workspace in-sync with the remote
repository.

If there are uncommitted changes in your workspace, shown by `git
status` command, they should be either discarded or saved for working
on them later. To discard the uncommitted changes, run

```
git checkout .
```

To save them for later use, run

```
git stash
```

Then pull the latest from upstream repository on gitlab.com.

```
git checkout main
git pull --rebase origin main
```

### Step 2: create a new branch

Each logical code change comprises of one of more commits. Branches
in git are used to group these commits, iterate on them, test them and
so on. Taking the example above, let's name our new branch as
`dev`.

```
git checkout -b dev
```

### Step 3: make code changes

Ensure that you're on the right branch, before changing anything.

```bash
git checkout dev
# The following command shows current branch
git branch
```

The above command should show `dev` as your current branch.
Code changes can now be made by editing existing files in your
workspace. New files can be created. Once the chagnes are tested,
inspect the changed files as follows.

```
git diff
```

This command shows the edits made so far to existing files, with
respect to the head of current branch, which should be
`dev`. If the diff looks as expected, and your tests pass,
commit the changes as follows.

```bash
# For each newly created file
git add <new file>
# For changes to existing files
git add -u
```

The `git add` command stages the changes for commit. Inspect the
files staged for commit using `status` command:

```
git status
```

The next step is to commit the staged changes. The `commit` command
needs a commit message. Commit message should mainly include _why_
the change is being made. A common mistake is to describe what is
being changed. What's being changed can be seen with `git show`. The
intention behind the code change is hidden in the author's mind and
should be described in the commit message.

```
git commit
```

### Step 4: create merge request

Merge requests allow your changes to be published within the team so
that they can be reviewed. Merge requests can be created by pushing
the feature branch (`dev`) to remote repository on
gitlab.com.

```bash
# Fetch any new changes from remote / upstream
git fetch origin
# Ensure that you're on the right branch
git checkout dev
# Rebase your commits on top of the newly fetched changes from remote
git rebase origin/main
```

The `rebase` command may report conflits. This happens when same part
of the files edited by your changes have also been changed on remote.
The conflicts need to be resolved manually, once for each new commit
in your feature branch. Once all conflicts are resoled, you're ready
to push.

```
git push origin dev
```

At this point, your branch is available on gitlab.com remote. Use the
[create merge request
link](https://gitlab.com/iitb/webapps/-/merge_requests/new) with
`main` as target branch and feature branch `dev` as source
branch. Share the merge request link within your team.

### Step 5: incorporate review comments

Team members may provide comments on your merge request. The comments
may need you to make further code changes. In that case, make new
commits as mentioned in Step 3. Once you've tested the new commits,
push the feature branch from your workspace to remote, so that the new
commits can be reviewed from the same merge request.

```
git push origin dev
```

Post a comment on the merge request to notify your team members to
take another look at the code changes.

### Step 6: merge approved merge-request into main branch

Once the merge request is approved by one or more team members, the
feature branch should be merged into main branch. Before this can be
done, any new changes that might have happened on `main` branch in
remote must be pulled. Commits in the feature branch need to be
rebased on top of the newly pulled commits, as follows.

```
git checkout dev
git fetch origin main
git rebase origin/main
```

Resolve conflicts, if any. Test the code changes. If all tests pass,
you are ready to merge into main.

```bash
# Push feature branch so that the merge request is
# automatically closed by GitLab (after the last command below).
git push --force-with-lease origin dev
# Merge feature branch into main without creating a merge commit (--ff-only)
git checkout main
git merge --ff-only dev
# Push the modified main branch to remote repository
git push origin main
```

The merge request should automatically be closed by GitLab.com at this
point. If not, close the merge request manually.

### Step 7: delete the feature branch

After merging a feature branch into main, it should be discarded.

```bash
git checkout main
# Delete the branch from your workspace
git branch -D dev
# Delete the branch from remote repository
git push origin :dev
```