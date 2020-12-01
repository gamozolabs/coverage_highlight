#!/usr/bin/env python3

import os
import json

# Perform coverage highlighting
def coverage_highlight():
    # The json coverage format
    coverage_filename = ".coverage.json"

    # Make sure the file exists, and silently exit if it does not
    if not os.path.isfile(coverage_filename):
        return

    # Get the filename for this vim buffer
    current_buffer_fn = os.path.basename(vim.current.buffer.name)

    # Assign the first sign identifier. These will be allocated for each line
    # as we notice coverage on them. This is effectively a unique identifier
    # for the sign we create on each covered line
    sign_id = 1

    # Establish a group name based on the current vim buffer name
    sign_group = f"coverage_highlight_{current_buffer_fn}"

    # Enumerate all of the lines in the lcov
    for (fn, lines) in json.load(open(coverage_filename)).items():
        # Make sure the coverage file matches our current file open in the
        # VIM buffer
        if fn.endswith(current_buffer_fn) or current_buffer_fn.endswith(fn):
            # Go and highlight each line!
            for line_number in lines:
                vim.command(f"exe \":sign place {sign_id} line={line_number} \
                        group={sign_group} priority=9999 \
                        name=covered_line_color file=\".expand(\"%:p\")")
                sign_id += 1

