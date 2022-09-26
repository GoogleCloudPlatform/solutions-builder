#!/bin/bash
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/bash

set -f

HEADER_BLOCK=$(cat <<-END
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
END
)

PYTHON_HEADER_BLOCK=$(cat <<-END
"""
Copyright 2022 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
END
)

JS_HEADER_BLOCK=$(cat <<-END
/**
 * Copyright 2022 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */
END
)

HTML_HEADER_BLOCK=$(cat <<-END
<!--
Copyright 2022 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->
END
)

SHELL_HEADER_BLOCK=$(cat <<-END
#!/bin/bash
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
END
)


print_help() {
  echo
  echo "Usage: ./add_header.sh [Folder Path] [File Pattern]"
  echo
  echo "Example: ./add_header.sh . '*.py'"
  echo
}

add_headers() {
for fname in `find $1 -name "$2" ! -name "__init__.py" ! -path "*/node_modules/*" ! -path "*/.terraform/*"`; do
  echo "Adding header to: $fname"
  if [[ "$fname" == *.ts || "$fname" == *.js || "$fname" == *.css || "$fname" == *.tf ]]; then
    HEADER_BLOCK=$JS_HEADER_BLOCK
  elif [[ "$fname" == *.py ]]; then
    HEADER_BLOCK=$PYTHON_HEADER_BLOCK
  elif [[ "$fname" == *.sh ]]; then
    HEADER_BLOCK=$SHELL_HEADER_BLOCK
  elif [[ "$fname" == *.html || "$fname" == *.htm ]]; then
    HEADER_BLOCK=$HTML_HEADER_BLOCK
  fi

  if grep -q "Copyright 2022 Google LLC" $fname; then
    echo "${fname} already has license header. Skipped."
    continue
  fi

  cat - $fname > /tmp/f.py <<EOF
$HEADER_BLOCK

EOF
  mv /tmp/f.py $fname
done
}

if [ -z "$1" ] | [ -z "$2" ]
then
  print_help
  exit 1
fi

counter=0
echo "About to add headers to the following files:"
echo
for fname in `find $1 -name "$2" ! -name "__init__.py" ! -path "*/node_modules/*" ! -path "*/.terraform/*"`; do
  echo "$fname"
  let counter++
done

echo
echo "Total $counter files. Continue (y/n)?"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
  add_headers $1 $2
  echo
  echo "Complete"
else
  echo "Aborted"
fi
