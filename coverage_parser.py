#!/usr/bin/env python3

import os
import json
import binascii

# Perform coverage highlighting
def coverage_highlight():
    # The json coverage format
    coverage_filename = ".coverage.json"

    # Get the filename for this vim buffer
    current_buffer_fn = os.path.basename(vim.current.buffer.name)

    # Assign the first sign identifier. These will be allocated for each line
    # as we notice coverage on them. This is effectively a unique identifier
    # for the sign we create on each covered line
    sign_id = 1

    # Establish a group name based on the current vim buffer name
    # Hexlify it to remove all special characters, spaces, etc. This is a
    # simple way to "escape" the name to make a unique identifier
    sign_group = \
        binascii.hexlify(f"coverage_highlight_{current_buffer_fn}".encode())

    # Clear all signs which match the sign group for this file. This will
    # delete all previous coverage highlights which allows a file to be
    # refreshed and coverage will also be refreshed
    vim.command(f"exe \":sign unplace * group={sign_group} \
        file=\".expand(\"%:p\")")

    try:
        # Enumerate all of the lines in the lcov
        for (fn, lines) in json.load(open(coverage_filename)).items():
            # Make sure the coverage file matches our current file open in the
            # VIM buffer
            if fn.endswith(current_buffer_fn) or \
                    current_buffer_fn.endswith(fn):
                # Go and highlight each line!
                for line_number in lines:
                    vim.command(f"exe \":sign place {sign_id} \
                            line={line_number} \
                            group={sign_group} priority=9999 \
                            name=covered_line_color file=\".expand(\"%:p\")")
                    sign_id += 1
    except FileNotFoundError:
        pass

