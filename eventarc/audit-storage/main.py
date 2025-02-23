# Copyright 2020 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START eventarc_audit_storage_server]
import os
import json

from flask import Flask, request


app = Flask(__name__)
# [END eventarc_audit_storage_server]


# [START eventarc_audit_storage_handler]
@app.route('/', methods=['POST'])
def index():
    # Gets the GCS bucket name from the CloudEvent header
    # Example: "storage.googleapis.com/projects/_/buckets/my-bucket"
    bucket = request.headers.get('ce-subject')

    print('request', request)
    print('type(request.headers)', type(request.headers))
    print('request.headers', request.headers)
    filename = bucket.split('/', 1)[1]
    print('filename', filename)

    source = request.headers.get('ce-source')
    print('source', source)
    bucket_name = source.split('/')[-1]
    print('bucket_name', bucket_name)

    full_path = f"gs://{bucket_name}/{filename}"
    print('full_path', full_path)

    print(dir(request))
    if hasattr(request, 'data'):
        print(request.data)
    
    d = json.loads(request.data)
    print(d['bucket'])
    print(d['name'])
    print(f"gs://{d['bucket']}/{d['name']}")

    print(f"Detected change in Cloud Storage bucket: {bucket}")
    return (f"Detected change in Cloud Storage bucket: {bucket}", 200)
# [END eventarc_audit_storage_handler]


# [START eventarc_audit_storage_server]
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
# [END eventarc_audit_storage_server]
