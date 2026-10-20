"""Verify self-contained examples without pretending to run distributed engines."""
import pytest
from markdown_it import MarkdownIt
from scripts.validate import ROOT

LOCAL_EXAMPLES = [
    'foundations/distributed-computing.md',
    'distributed-systems/partitioning.md',
    'distributed-systems/data-skew.md',
    'processing/incremental-data-loading.md',
]


@pytest.mark.parametrize('relative', LOCAL_EXAMPLES)
def test_local_example_assertions(relative):
    path = ROOT / 'docs' / relative
    blocks = [token.content for token in MarkdownIt().parse(path.read_text())
              if token.type == 'fence' and token.info == 'python']
    assert blocks, f'{relative} lost its executable example'
    for block in blocks:
        exec(compile(block, str(path), 'exec'), {})


def test_external_spark_example_compiles_without_claiming_execution():
    path = ROOT / 'docs/processing/apache-spark.md'
    blocks = [token.content for token in MarkdownIt().parse(path.read_text())
              if token.type == 'fence' and token.info == 'python']
    assert blocks
    for block in blocks:
        compile(block, str(path), 'exec')
