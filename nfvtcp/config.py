"""
Copyright (c) 2017 Manuel Peuster
ALL RIGHTS RESERVED.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Manuel Peuster, Paderborn University, manuel@peuster.de
"""
import logging
import os
import yaml
import sys

LOG = logging.getLogger(os.path.basename(__file__))


def read_config(path):
    try:
        with open(path, "r") as f:
            conf = yaml.load(f)
            # do some basic validation on config
            assert("name" in conf)
            assert("author" in conf)
            assert("version" in conf)
            assert("max_time_t" in conf)
            assert("repetitions" in conf)
            assert("pmodels" in conf)
            assert("selector" in conf)
            assert("predictor" in conf)
            assert("error_metrics" in conf)
    except AssertionError as e:
        LOG.exception("Couldn't parse config '{}' {}".format(path, e))
        LOG.error("Abort.")
        sys.exit(1)
    except Exception as e:
        LOG.exception("Couldn't parse config '{}' {}".format(path, e))
        LOG.error("Abort.")
        sys.exit(1)
    LOG.info("Loaded configuration: {}".format(path))
    return conf


def expand_parameters(p):
    """
    Expand single values, lists or dicts to a
    list of parameters.
    """
    if p is None:
        return [None]
    if isinstance(p, int) or isinstance(p, float):
        return [p]
    elif isinstance(p, list):
        return p
    elif isinstance(p, dict):
        try:
            assert("min" in p)
            assert("max" in p)
            assert("step" in p)
            # TODO support floats
            # attention: we do range(min, max+1)
            return list(range(p.get("min"), p.get("max") + 1, p.get("step")))
        except:
            LOG.exception("AssertionError in dict expansion")
    raise ValueError("cannot expand config parameter: {}".format(p))
