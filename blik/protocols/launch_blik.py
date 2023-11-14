#!/usr/bin/env python3

from pathlib import Path
import argparse

import napari
import warnings
from napari.plugins.io import save_layers
from magicgui import magicgui
from magicgui.widgets import Container


SAVE_ALL_SHORTCUT = 'Alt+a'


parser = argparse.ArgumentParser()
parser.add_argument('input_files', nargs='+', type=Path)
parser.add_argument('-o', '--output-directory', required=True, type=Path)
args = parser.parse_args()


def _save_particle_layers_with_blik(layers, strict=True):
    # need to get unique names... this would be so much easier if we could just speak
    # to scipion directly via python :( for now, just have an index that's higher than
    # the number of files.
    current_counter = len(list(Path(args.output_path).glob('*_particle_picks_*.star')))
    for layer in layers:
        experiment_id = layer.metadata.get('experiment_id', None)
        if not isinstance(layer, napari.layers.Points) or experiment_id is None:
            if not strict:
                continue  # otherwise, it will raise in the next line
        save_layers(
            path=args.output_path / f'{experiment_id}_particle_picks_{current_counter}',
            layers=layers,
            plugin='blik'
        )
        current_counter += 1


@magicgui(call_button='Save', layout='horizontal')
def save_particles(particle_layer: napari.layers.Points):
    """Save a single particle set to the Scipion output directory."""
    _save_particle_layers_with_blik([particle_layer])


@magicgui(call_button=f'Save all particle layers ({SAVE_ALL_SHORTCUT})')
def save_all_particles(viewer: napari.Viewer):
    """Save all particles in the viewer to the Scipion output directory."""
    _save_particle_layers_with_blik(viewer.layers, strict=False)


container = Container(widgets=[save_particles, save_all_particles], labels=False)

viewer = napari.Viewer()
widget = viewer.window.add_dock_widget(container, name='Save for Scipion')
# shortcut for covenience
viewer.bind_key(SAVE_ALL_SHORTCUT, overwrite=True)(lambda x: save_all_particles(viewer))

# make it harder for users to mess up by closing the widget
widget.title.close_button.hide()
widget.title.hide_button.hide()
widget.title.float_button.hide()

# open all the input tomograms
layers = viewer.open(args.input_files, plugin='blik')

napari.run()
