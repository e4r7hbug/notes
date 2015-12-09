#!/usr/bin/env python
"""Sampling how to test Git repository hooks."""
import logging
import os
import shutil
import stat
import tempfile

from IPython import embed

from git import Repo


class TempRepo(object):
    """Autoclean up a temporary directory."""
    clone = None
    log = logging.getLogger(__name__)
    path = ''
    repo = None

    def __init__(self, bare=False):
        self.log.info('INIT')
        self.path = tempfile.mkdtemp(suffix='.git')
        self.repo = Repo.init(self.path, bare=bare)

        clone_dir = tempfile.mkdtemp(suffix='.git')
        self.clone = self.repo.clone(clone_dir)

    def __enter__(self):
        self.log.info('ENTER')
        return self

    def __exit__(self, exit_type, exit_value, exit_traceback):
        self.log.info('EXIT')
        shutil.rmtree(self.path)
        shutil.rmtree(self.clone.working_dir)

    def update_script(self):
        """Install an update script into a bare repo.

        Returns:
            Path string to update hook.
        """
        update_file = os.path.join(self.repo.git_dir, 'hooks', 'update')

        if self.repo.bare:
            with open(update_file, 'w+') as hook:
                hook.write(
                    '#!/usr/bin/env python\nimport sys\nprint(sys.argv)')
            os.chmod(update_file, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

        return update_file

    def create_test_file(self):
        """Create test file in repository.

        Returns:
            Path string to new file.
        """
        test_file = os.path.join(self.clone.working_dir, 'test')

        with open(test_file, 'w+') as test_file_handle:
            test_file_handle.write('sample')

        return test_file


def main():
    """Main."""
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger(__name__)

    with TempRepo(bare=True) as bare_repo:
        log.info('Bare repo = %s', bare_repo.path)
        clone = bare_repo.clone
        log.info('Clone = %s', clone.working_dir)

        bare_repo.update_script()
        bare_repo.create_test_file()

        clone.index.add(clone.untracked_files)
        clone.index.commit('Test commit')

        origin = clone.remote()
        status = origin.push()

        embed()


if __name__ == '__main__':
    main()
