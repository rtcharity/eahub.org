# Contributing to EA Hub  

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:  

## Code of Conduct  
Please find our [Code of Conduct](CODE_OF_CONDUCT.md) here. By participating in the EA Hub project you are expected to 
uphold this code. Please report anny violations to [tech@eahub.org](mailto:tech@eahub.org).  

## How Can I Contribute?  

### Reporting Bugs  
Reporting bugs helps us continuously improve the EA Hub.  

If you think you've found a bug, please check first [here](https://github.com/rtcharity/eahub.org/labels/Bug) whether it 
has already been reported.  

If the bug has not been reported, please [raise a GitHub issue](https://github.com/rtcharity/eahub.org/issues/new). Please 
give as much information as possible:  
* Use a clear and descriptive title for the issue to identify the problem.  
* Describe the exact steps which reproduce the problem with as much detail as possible.  
* Describe the behaviour you observed after following these steps.    
* Explain which behaviour you expected to see and why.  
* Provide a screenshot of the bug.  
* Give information about your environment (browser, device, screen width, operating system, etc.)  

### Suggesting Enhancements  
You can suggest new features and other improvements on [meta.eahub.org](https://meta.eahub.org/c/feature-requests/). You 
will have to sign up first.  

### Your First Code Contribution  
The EA Hub is an open source project and we welcome developers to make contributions. You can find a list of first good 
GitHub issues to work on [here](https://github.com/rtcharity/eahub.org/labels/Good%20First%20Issue).  

If you'd like to work on one of these GitHub issues or would like to pick up another of 
[our GitHub issues](https://github.com/rtcharity/eahub.org/issues), **please first get in touch with us** so that we 
can discuss which issue would be ideal for you to work on and help you in case you have any questions. To get in touch, 
join the [contributions channel](https://discord.gg/CQueVjk3fc) on EA Hub's discord server and post a short message 
that you'd like to contribute.  

### Pull Requests  
To make a pull request, please fork the repo, create a branch on your fork and then make a PR into the main repo. For a detailed tutorial, please see our Contribution Tutorial at the end of this page.

When making a pull request, put yourself in the shoes of the reviewer and think what information they need to review 
your code effectively.  

In particular, please make sure that:    

1. The pull request has a clear and meaningful title
1. You've referenced the GitHub issue the pull request is addressing  
1. The pull request description:  
- Mentions which changes were made. Where applicable, make clear which changes are "core" changes, and which are just 
refactoring, styling changes etc.      
- Explains why these changes were made  
- Has screenshots of the relevant frontend changes (where applicable)    
1. All status checks have passed  

The Hub is fully run by volunteers, and it might take us some time to review your pull request. To help us review your 
pull request in a timely manner, please make sure to reach out to us first on the [contributions channel](https://discord.gg/CQueVjk3fc) 
and also mention to us there once your pull request is ready to review.  

### Git Commit Messages  
Since we have enabled squash-merging, all commits on your branch will be squashed into one when merging into master. 
Having clear commit messages on your branch will, however, make the code review easier. Hence, please follow the following 
guidelines (adapted from [here](https://chris.beams.io/posts/git-commit/)) for all commits, but especially for the final, 
squashed one:  
1. Separate subject from body with a blank line
1. Do not end the subject line with a period
1. Use the imperative mood in the subject line
1. Use the body to explain what and why vs. how  

## Contribution Tutorial

To commit changes to the main EAHub repo as a volunteer, you must create a pull request to merge your forked repo branch with the main EAHub repo. Here's how to do that!

### Setting up your forked repo and syncing it

This tutorial assumes you are using the command-line and already have git installed.

(1) Fork the [main EAHub repo](https://github.com/rtcharity/eahub.org) to your GitHub account, instructions here: https://docs.github.com/en/github/getting-started-with-github/quickstart/fork-a-repo (keep this doc open, it'll help you with most of the next steps)

(2) Make sure to clone your newly forked repo to your computer, see link from step 1 for instructions with pictures.

(3) Check your remote sources by entering the local directory representing that cloned git repo and running 

        git remote -v   

You should see something like "origin https://github.com/YOUR_USERNAME/YOUR_FORK.git" repeated on two lines with fetch at the end of one line and push at the end of the other line.

(4) Now clone the main EAHub repo to your computer inside a directory that DOES NOT contain your forked repo directory.

        git clone https://github.com/rtcharity/eahub.org.git

(5) Check the remote sources for that repo (they should be the github path / URL to the EAHub repo)
        
        git remote -v

(6) Change directories back to your forked repo. Then, add the main EAHub repo as a remote upstream:

        git remote add upstream https://github.com/rtcharity/eahub.org.git

(7) Check the remote sources for your forked repo, you should see your forked repo as origin and the main EAHub repo as upstream.

(8) [Make sure your forked repo (origin) is in sync with the main (upstream) EAHub repo](https://docs.github.com/en/github/collaborating-with-pull-requests/working-with-forks/syncing-a-fork) (Note: if you have unique commits on your local forked repo default branch, this shouldn't delete your local changes, but if something goes weird and their are merge conflicts, read how to [address merge conflicts](https://docs.github.com/en/github/collaborating-with-pull-requests/addressing-merge-conflicts) and troubleshoot accordingly) Aside: It is good to create a new branch when making local changes so that your local default branch stays the same as remote upstream main until you're ready to make your pull request.

        git fetch upstream
        git checkout main
        git merge upstream/main
(you may have to substitute "default" in place of main, since the default branch is usually called default)

(9) - As Needed - If you need to sync your local forked repo with your remote forked repo (origin) after syncing your local forked repo with the main (upstream), then [push your changes to your remote forked repo (origin)](https://docs.github.com/en/github/getting-started-with-github/using-git/pushing-commits-to-a-remote-repository) via

        git push origin main
        
(10) You should be ready to start working on your local forked repo and make whatever changes you wish to make! [Make a new branch](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-and-deleting-branches-within-your-repository#creating-a-branch) to do your work in and get started. You can do so using GitHub or [via terminal](https://zepel.io/blog/how-to-create-a-new-branch-in-github/#create-branch-command-line) (I prefer via terminal, it's faster):

        git branch "branch name"
        git checkout "branch name"
        
Much of these instructions were taken from [GitHub Docs' "Collaborating with pull requests"](https://docs.github.com/en/github/collaborating-with-pull-requests), they are a great reference guide and you should keep them handy especially if you're not too comfortable with git nor GitHub yet.

## Create a pull request to merge your forked repo branch with the main EAHub repo

This section assumes you have changes added and committed in your forked local git repo which you've pushed from your local git repo to your forked remote (on GitHub) repo, aka origin. 

(1) Please open and read / keep handy for reference GitHub's ["Creating a pull request from a fork"](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork) guide.

(2) Go to https://github.com/rtcharity/eahub.org/pulls

(3) Click "Create Pull Request" and under "Compare changes", click on "compare across forks"

(4) Select rtcharity/eahub.org as the "base repository" then select the appropriate branch as the "base" (likely the "default" branch).

(5) Select your forked repo as the "head repository" then select the branch you made changes to as the "compare".

(6) Click "Create Pull Request"

(7) Review the Pull Requests section above and make any necessary changes to ensure your pull request matches our style and follows our guidelines.