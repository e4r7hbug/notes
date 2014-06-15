# SaltStack
## Install
Depending on which parts of SaltStack you want to run, choose from:

* `salt-master` for running a Master Server to control Minions or Syndics
* `salt-minion` for running a Minion Client to be controlled
* `salt-syndic` allows target Master to control Host Master's Minions

```bash
root@machine:~# add-apt-repository -y ppa:saltstack/salt
root@machine:~# apt-get update
root@machine:~# apt-get install -y [salt-master] [salt-minion] [salt-syndic]
```

## Minion Configuration
Make sure to add `master: salt.trib` to `/etc/salt/minion` to target this Master.

```yaml
# Set the location of the salt master server, if the master server cannot be
# resolved, then the minion will fail to start.
#master: salt
master: salt.trib
```

Then, restart `salt-minion` service.

```bash
root@machine:~# service salt-minion restart
```

## Master Configuration
### Accept Keys
* Use `salt-key` to show all keys associated with this Master.
* `salt-key -A` will prompt to accept all keys

### Testing Testing
Check that all your Minions are responding with `True`.

```bash
salt '*' test.ping
```

## Salt States
Enable the default `file_roots` by uncommenting the lines in `/etc/salt/master`. This is where your Salt States go for default machine configurations. This `environment` is named `base`.

```yaml
file_roots:
  base:
    - /srv/salt
```

Make sure that directory exists.

```bash
root@salt:~# mkdir -p /srv/salt/
```

Restart the `salt-master` service to pickup the new configuration.

```bash
root@salt:~# service salt-master restart
```

### `top.sls`
The directory you defined in `file_roots` is where you would want to put your `top.sls` file. By default, Salt looks for this file based on the path you specified for the `environment`. In this case, we're going to be working in `/srv/salt`, the default commented location provided in the `/etc/salt/master` configuration file.

```bash
root@salt:/srv/salt# vim top.sls
```

```yaml
base:
  '*':
    - common
    - utils
  'tinyTower':
    - nate
  'db.trib':
    - db
```

* `base` is the name of your `environment`, this must match your `/etc/salt/master` configuration
* Second tier keys are matching strings for your Minions
* Third tier keys match your state files

   ```bash
   root@salt:/srv/salt# tree
   .
   ├── bash
   │   ├── bash.bashrc
   │   └── init.sls
   ├── common.sls
   ├── db.sls
   ├── docker
   │   └── init.sls
   ├── mysql
   │   └── init.sls
   ├── nate.sls
   ├── ppa
   │   ├── atom.sls
   │   ├── init.sls
   │   ├── profile-sync-daemon.sls
   │   └── variety.sls
   ├── ssh
   │   ├── init.sls
   │   └── sshd_config
   ├── top.sls
   └── utils.sls

   5 directories, 15 files
   ```

   * use directory name if it contains a `init.sls` file, e.g. `bash` refers to `bash/init.sls`
   * use front part of `.sls` filenames if file is in root path, e.g. `utils` refers to `utils.sls`
   * use `directory.file` if targeting a deeper `.sls` file, e.g. `ppa.atom` refers to `ppa/atom.sls`
