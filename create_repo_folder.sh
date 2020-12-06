#!/bin/sh
# make sure we're in the correct path
working_path=$(cd $HOME/development/GitHub/)
# dir=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
echo $working_path


# create new folder using user input
read -p 'Please enter folder name: ' new_folder
new_path=$(mkdir -p $working_path/$new_folder)

# now we switch to our newly created directory
echo $new_folder
echo $working_path
cd $new_path

# # Tell git to watch this foler for changes
# if [ -d $new_path ]; then
#   # Create a new README.md for project
#   $echo "Give a short desription of your project"
#   read -p 'Desription: ' prj_description
#   # Now send that to the readme.md file
#   echo $prj_description > README.md
#   # Let's initialise git in our new folder.
#   git init
#   git commit -am "Add README.md"
#   hub create
#   git push -u origin HEAD
# else
#   echo "Hmm...this is embarrasing. Let's try again."
# fi
