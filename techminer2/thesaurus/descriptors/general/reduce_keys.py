# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
# pylint: disable=too-many-branches
"""
Reduce Keys
===============================================================================


>>> from techminer2.thesaurus.descriptors import CreateThesaurus
>>> CreateThesaurus(root_directory="example/", quiet=True).run()


>>> from techminer2.thesaurus.descriptors import ReduceKeys
>>> (
...     ReduceKeys()
...     #
...     # DATABASE:
...     .where_root_directory_is("example/")
...     #
...     .run()
... )
Reducing thesaurus keys
  File : example/thesaurus/descriptors.the.txt
  Keys reduced from 1796 to 1796
  Keys reduction completed successfully
<BLANKLINE>




"""
from ...._internals.mixins import ParamsMixin
from ...user import ReduceKeys as UserReduceKeys


class ReduceKeys(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def run(self):
        (
            UserReduceKeys(
                thesaurus_file="descriptors.the.txt",
                root_directory=self.params.root_directory,
            ).run()
        )


# =============================================================================
