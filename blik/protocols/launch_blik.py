#!/usr/bin/env python3

from pathlib import Path
import argparse

import napari
from napari.plugins.io import save_layers
from napari.utils.notifications import show_info
from magicgui import magicgui
from magicgui.widgets import Container


SAVE_ALL_SHORTCUT = 'Alt-a'


parser = argparse.ArgumentParser()
parser.add_argument('input_files', nargs='+', type=Path)
parser.add_argument('-o', '--output-path', required=True, type=Path)
args = parser.parse_args()


def _save_particle_layers_with_blik(layers, raise_=True):
    # need to get unique names... this would be so much easier if we could just speak
    # to scipion directly via python :( for now, just have an index that's higher than
    # the number of files.
    current_counter = len(list(Path(args.output_path).glob('*_particle_picks_*.star')))
    saved = {}
    for layer in layers:
        experiment_id = layer.metadata.get('experiment_id', None)
        if not isinstance(layer, napari.layers.Points) or experiment_id is None:
            if not raise_:
                continue  # if strict, it will raise an informative error in the next line
        save_path = str(args.output_path / f'{experiment_id}_particle_picks_{current_counter}')
        save_layers(
            path=save_path,
            layers=[layer],
            plugin='blik',
        )
        saved[layer.name] = save_path
        current_counter += 1
    return saved


def _hide_widget_buttons(widget):
    widget.title.close_button.hide()
    widget.title.hide_button.hide()
    widget.title.float_button.hide()


@magicgui(call_button='Save', layout='horizontal')
def save_particles(particle_layer: napari.layers.Points):
    """Save a single particle set to the Scipion output directory."""
    saved = _save_particle_layers_with_blik([particle_layer])
    show_info(f'Saved {saved[0]} as {saved[1]}.')


@magicgui(call_button=f'Save all particle layers ({SAVE_ALL_SHORTCUT})')
def save_all_particles(viewer: napari.Viewer):
    """Save all particles in the viewer to the Scipion output directory."""
    saved = _save_particle_layers_with_blik(viewer.layers, raise_=False)
    show_info(f'Saved: {", ".join(saved)}.')


container = Container(widgets=[save_particles, save_all_particles], labels=False)

viewer = napari.Viewer()

# shortcut for covenience
viewer.bind_key(SAVE_ALL_SHORTCUT, overwrite=True)(lambda x: save_all_particles(viewer))

# scipion-specific widget
scipion_widget = viewer.window.add_dock_widget(container, name='Save for Scipion')
# open blik widget
blik_main_widget = viewer.window.add_plugin_dock_widget('blik')[0]

# make it harder for users to mess up by closing the widget
_hide_widget_buttons(scipion_widget)
_hide_widget_buttons(blik_main_widget)

# open all the input tomograms
layers = viewer.open(args.input_files, plugin='blik')

napari.run()
