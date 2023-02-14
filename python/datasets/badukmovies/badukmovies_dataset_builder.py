"""
badukmovies dataset.

Only contains unscored games!!!!

Dividing the dataset into scored/unscored games for faster loss calculations.
"""

from __future__ import annotations

import numpy as np
import resource
import tensorflow_datasets as tfds

low, high = resource.getrlimit(resource.RLIMIT_NOFILE)
resource.setrlimit(resource.RLIMIT_NOFILE, (low * 4, high))


class Builder(tfds.core.GeneratorBasedBuilder):
  """DatasetBuilder for badukmovies dataset."""

  MANUAL_DOWNLOAD_INSTRUCTIONS = """
  Download zip from badukmovies.com
  """

  VERSION = tfds.core.Version('1.0.0')
  RELEASE_NOTES = {
      '1.0.0': 'Initial release.',
  }

  def _info(self) -> tfds.core.DatasetInfo:
    """Returns the dataset metadata."""
    import datasets.common.constants as constants
    return self.dataset_info_from_configs(
        features=tfds.features.FeaturesDict({
            'metadata':
                tfds.features.Text(
                    doc='Metadata encoding information about the game played.'),
            'board':
                tfds.features.Tensor(
                    shape=(constants.BOARD_LEN, constants.BOARD_LEN),
                    dtype=np.int8,
                    doc=
                    '19x19 matrix representing board state from perspective of current player',
                ),
            'komi':
                tfds.features.Scalar(
                    dtype=np.float16,
                    doc=
                    'Komi from perspective of current player (0 for B, |K| for white).'
                ),
            'color':
                tfds.features.Scalar(
                    dtype=np.int8,
                    doc=
                    'Value representing current color to play (Black = 0, White = 1)',
                ),
            'result':
                tfds.features.Scalar(
                    dtype=np.int16,
                    doc=
                    'Value representing (score_diff - .5) from perspective of current player. \
                     result = 0 means that the current player won by .5 points. \
                     result = -500 means current player resigned. \
                     result = 500 means current player won by resignation. \
                     result = -1000 means unknown result.',
                ),
            'last_moves':
                tfds.features.Tensor(
                    shape=(constants.NUM_LAST_MOVES, 2),
                    dtype=np.int8,
                    doc='Last 5 moves, as tuples (i, j) indexing into `board`'),
            'policy':
                tfds.features.Tensor(shape=(2,),
                                     dtype=np.int8,
                                     doc='Tuple encoding the next move played'),
        }),
        supervised_keys=None,
    )

  def _split_generators(self, dl_manager: tfds.download.DownloadManager):
    """Returns SplitGenerators."""
    path = dl_manager.manual_dir / 'baduk'

    # TODO(badukmovies): Returns the Dict[split names, Iterator[Key, Example]]
    return {
        'train': self._generate_examples(path),
    }

  def _generate_examples(self, path: tfds.core.Path):
    """Yields examples."""
    import datasets.common.example_generator as example_generator
    generator = example_generator.ExampleGenerator(
        path, mode=example_generator.GeneratorMode.UNSCORED)
    return generator.generate()
