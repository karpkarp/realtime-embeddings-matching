#!/usr/bin/python
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask
from flask import request
from flask import jsonify
from utils import search as srch

search_util = srch.SearchUtil()

app = Flask(__name__)


@app.route('/')
def display_default():
  return 'Welcome to the semantic search app!\n' \
         'use /search?query=<your_query> to start searching to articles'


@app.route('/readiness_check')
def check_readiness():
  return 'App is ready!'


@app.route('/search', methods=['GET'])
def search():
  try:
    query = request.args.get('query')
    show = request.args.get('show')
    show = '10' if show is None else show

    is_valid, error = validate_request(query, show)

    if not is_valid:
      results = error
    else:
      results = search_util.search(query, int(show))

  except Exception as error:
    results = 'Unexpected error: {}'.format(error)

  response = jsonify(results)
  return response


def validate_request(query, show):
  is_valid = True
  error = ''

  if query is None or len(query) < 3:
    is_valid = False
    error = 'Your search query is too short!'
  elif show is None or not show.isdigit():
    is_valid = False
    error = 'Invalid show results value!'

  return is_valid, error


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5000, debug=True)
