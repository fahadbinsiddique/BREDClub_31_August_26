import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PYTHON_EXECUTABLE = sys.executable or 'python'


def run_command(command):
    subprocess.check_call(command, cwd=ROOT, shell=True)


def build_manage_command(*args):
    return f'"{PYTHON_EXECUTABLE}" manage.py ' + ' '.join(args)


def main():
    run_command(build_manage_command('migrate'))
    run_command(build_manage_command('create_admin', '--username', 'admin', '--email', 'admin@bredclub.org', '--password', 'admin123'))
    run_command(build_manage_command('seed_site_content'))
    run_command(build_manage_command('seed_sample_content'))
    run_command(build_manage_command('seed_gallery_content'))
    print('Project setup completed successfully.')


if __name__ == '__main__':
    main()
