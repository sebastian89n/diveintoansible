# (c) 2012, Jeroen Hoekx <jeroen@hoekx.be>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

import base64
import functools
import glob
import hashlib
import json
import ntpath
import os.path
import re
import shlex
import time
import uuid
import yaml
import datetime
import typing as t

from collections.abc import Mapping
from functools import partial
from random import Random, SystemRandom, shuffle

from jinja2.filters import do_map, do_select, do_selectattr, do_reject, do_rejectattr, pass_environment, sync_do_groupby
from jinja2.environment import Environment

from ansible._internal._templating import _lazy_containers
from ansible.errors import AnsibleFilterError, AnsibleTypeError, AnsibleTemplatePluginError
from ansible.module_utils.datatag import native_type_name
from ansible.module_utils.common.json import get_encoder, get_decoder
from ansible.module_utils.six import string_types, integer_types, text_type
from ansible.module_utils.common.text.converters import to_bytes, to_native, to_text
from ansible.module_utils.common.collections import is_sequence
from ansible.parsing.yaml.dumper import AnsibleDumper
from ansible.template import accept_args_markers, accept_lazy_markers
from ansible._internal._templating._jinja_common import MarkerError, UndefinedMarker, validate_arg_type
from ansible._internal._yaml import _loader as _yaml_loader
from ansible.utils.display import Display
from ansible.utils.encrypt import do_encrypt, PASSLIB_AVAILABLE
from ansible.utils.hashing import md5s, checksum_s
from ansible.utils.unicode import unicode_wrap
from ansible.utils.vars import merge_hash

display = Display()

UUID_NAMESPACE_ANSIBLE = uuid.UUID('361E6D51-FAEC-444A-9079-341386DA8E2E')

def reverse_upper(string):
    '''Reverse and upper string'''
    return string[::-1].upper()

class FilterModule(object):
    """ Ansible core jinja2 filters """

    def filters(self):
        return {
            'reverse_upper': reverse_upper
        }
