"""
This file allows running the parent directory directly:
python3 src [ arg1 ... ]

This also allows packaging up as a zipapp.

If you do not need this functionality:
  - Remove this file.
  - Consider moving mftscleanup out of src.
"""

import mftscleanup.__main__

mftscleanup.__main__.main()
