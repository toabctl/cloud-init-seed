#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright 2018 Thomas Bechtold <thomasbechtold@jpberlin.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import os
import subprocess
import tempfile
import uuid


USER_DATA = """#cloud-config
debug=True
ssh_authorized_keys:
  - {}
"""

META_DATA = """instance-id: {}
local-hostname: cloudy
"""

def create(args):
    with tempfile.TemporaryDirectory() as tempdir:
        with open(os.path.join(tempdir, 'user-data'), 'w') as ud:
            ud.write(USER_DATA.format(args.ssh_pub_key.read()))
        with open(os.path.join(tempdir, 'meta-data'), 'w') as md:
            md.write(META_DATA.format(uuid.uuid4()))
        args = ['/usr/bin/mkisofs',
                '-output', args.outfile,
                '-volid', 'cidata',
                '-joliet', '-rock',
                tempdir]
        subprocess.check_call(args, stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)


def parse_args():
    parser = argparse.ArgumentParser(
        description='cloud-init seed image creation')
    subparsers = parser.add_subparsers(help='sub-command help')

    # create
    parser_create = subparsers.add_parser(
        'create', help='Create an cloud-init compatible seed image')
    parser_create.add_argument('--outfile', type=str, default='seed.img',
                              help='Path to the output seed file. Defaults'
                              ' to %(default)s')
    parser_create.add_argument('--ssh-pub-key',
                               type=argparse.FileType('r'),
                               default=os.path.expanduser('~/.ssh/id_rsa.pub'),
                               help='Path to the ssh public key file. '
                               'Defaults to "%(default)s"')
    parser_create.set_defaults(func=create)

    return parser.parse_args()


def main():
    args = parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
