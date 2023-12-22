#!/bin/bash
  python3 manage.py migrate

  uwsgi --emperor /etc/uwsgi/vassals --uid root --gid root --enable-threads --daemonize /usr/workspace/mongo/uwsgi-emperor.log

  service nginx restart
