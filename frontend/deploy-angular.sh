#!/bin/bash
# This script is to automate the building of the angular frontend

cd angular-src
echo "Building angular source in prod mode"
ng build --prod
cd ../
echo "Copying contents of dist into static files"
cp -R angular-src/dist/. ../backend/dist/
echo "Finished copying"
cd ../backend
echo "Do you want to deploy to heroku? [yes/no]"
read deploy

if [ $deploy == "yes" ]
then
    git add .
    git commit -m "deploy"
    echo "git committed"
    echo "preparing to push to heroku"
    git push heroku master
    echo "done, deployed to heroku"
    cd ../
else
    echo "done, did not deploy to heroku"
    cd ../
fi