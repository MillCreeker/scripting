# Template Repository

## About
### Authors/Contributors
* [Michael Ulm](mailto:michael.ulm@fh-joanneum.at)
* [Harald Schwab](mailto:harald.schwab2@fh-joanneum.at)

### Description
> What will we do
This is a template repository for our students, to offer a showcase how a exercise/project repository should look like and which necessary points should be covert by the README.

This "project" contains/will implement/focus on:
* Simple structure for a git repo
* Example for useful README
* helpful start point for our students
* ...

## Installation/Prerequisites for your repository
1. clone this repository
  ```bash
  git clone <URL> [my_project]
  ```
2. remove `.git` folder to start with a 'clean' repo
  ```bash
  cd my_project
  rm -rf .git
  ```
3. change [README](README.md) to your needs (keep headlines)
4. init local git repository
  ```bash
  git init
  git add .
  git commit -m "initial commit"
  ```
5. create a new project on [git-iit](https://git-iit.fh-joanneum.at)
6. push local repository to remote
  ```bash
  git remote add origin <git@git-iit.fh-joanneum.at:<your-user/group>/repo-name.git>
  git push --set-upstream origin master
  ```

## Run/Execute
If necessary, add also a description how to run/execute your project/program/script/etc.

> e.g. add possible run options
```bash
# run script with additional output
./script.py -v
```

> or describe you to setup the configuration...
### Custom Configuration
to connect to your database, copy the `src/config/db.conf.example` to `src/config/db.conf` and change the needed parameters.

to run the server on a specific port, add a `.env` file in the project root and add a `PORT` variable with the desired port:

**.env**
```env
PORT=8080
```

...

## Documentation
> What have we done...

## Known Issues
Document any known issues in the README, so that for everyone is clear which already explored problems could appear.

> If possible, for a quick fix provide a workaround, on a long-range the bug/issue should be fixed and the README updated!


## Useful links
> provide (especially for yourself) useful links, that helped you during the development
* [Other README template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* 