# Lab2cRobot-Beta
This repository is just for test</br>
   # 1. Download git bash</br>
   # 2. Config your github account and github email by</br>
   ```
     git config --global user.name:yourusername
     git config --global user.email:youremail   
   ```
   "--global" means this account will be used for all git repo on this computer. </br>
   # 3. generate ssh key by</br>
   ```
   cd ~/.ssh
   ssh-keygen -t rsa -C "your_email@example.com"
   ```
   I suggest you naming the file that restore the key as "id_rsa"</br>  
   # 4. Try</br>
   ```
   ssh-add id_rsa # try this if it says 'Permission denied (publickey)'.
   ssh -T git@github.com
   ```
   If you see "Hi yourname You've successfully authenticated, but GitHub does not provide shell access. ",
   you are connected to Github now.</br>
   # 5. Use ```git clone 'git@github:repositeryname' ``` to clone this repo to your laptop</br>
   You can find relative link which should be in '' by clicking the button "clone or download". </br>
   # 6. After succeesfully clone
   You can use  
   ```cd Lab2cRobot-Beta``` switch to the repositery(master branch). Just tap "lab" and press "tab", git bash will complete it</br>
   To keep code in master branch always work, please create and work on a new branch.
   ```git branch new branch``` Creat a new branch
   ```git checkout branchname``` Switch to a branch
   ```git checkout -b new_branch_ha``` Creat and switch to the new branch
   # 7. Add, commit, push and pull. 
   At the first time you will creat a branch and work on it. 
   During your work, you can use ```git add``` to save your to Staged(now your work is in working directory).</br>
   ```git add .``` will save new files and modified files, but not deleted files.</br>
   ```git add -u``` will save new files and deleted files, but not modified files.</br>
   ```git add -A``` will save all changes.</br>
   ```git add filename``` will add specific files.</br> 
   ```git status``` can show you status of your files.</br>
   'Untracked' means files are in work directory and not tracked by git. After ```git add```, they will become 'modified'</br>
   'Staged' means files are staged but not submit to remote repositery.</br>
   Use ``` git commit -m "message"``` to submit staged changes to repositery.</br>
   After you finish your work, use ```git push origin yourbranchname ``` to send it Our repositery.</br>  
   When you want to commit, make sure you have finished at least one function or a method.</br>
   When you want to commit, make sure all jobs have been done and their is no bug.</br>
   </br>
   To your branch from remote repo, use ```git pull origin branchname```. 
   # 8. Merge 
   Don't merge branches by yourself. Please use Issue in github to request merge. </br>
   nner-group branches should first be merged by group leaders and Yihua will take care of merge of inter-group branches.</br>
   First switch to the branch you want to keep, then use</br>
   ```git merge branchname``` to merge branches.
   # 9. Merge conflicts
   Merge conflicts will appear when git fail to figure out which version of codes you want to save.</br>
   It means codes in repositery is different from what you pull from it.

   # Finally, Google or Baidu when things go wrong.

   # Tip. Usage on git command
   You can check the ** git-cheatsheet.pdf ** for common git command
