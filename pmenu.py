#!/usr/bin/env python
'''
a tiny pulseaudio sink switcher written in python. 

requires dmenu and integrates nicely with i3.

example key binding:
  bindsym $mod+shift+a exec --no-startup-id /path/to/pmenu.py

inspired by https://github.com/bannana/pmenu
'''
import sys
from pulsectl import Pulse, PulseVolumeInfo
from dmenu import dmenu

pulse = Pulse()

sink_inputs = pulse.sink_input_list()
sinks = pulse.sink_list()

if len(sinks) < 2:
    sys.exit(0)

sink_input_dmenu_list = ['{0:02d} - {1} ({2})'.format(x, y.name, y.proplist['application.process.binary'])
                          for (x, y) in enumerate(sink_inputs)]
sink_dmenu_list = ['{0:02d} - {1} ({2:.0%})'.format(x, y.name, y.volume.value_flat)
                   for (x, y) in enumerate(sinks)]

sink_input_index = int(dmenu.show(sink_input_dmenu_list, lines=len(sink_inputs)).split(' - ')[0])
sink_index = int(dmenu.show(sink_dmenu_list, lines=len(sinks)).split(' - ')[0])

pulse.sink_input_move(sink_inputs[sink_input_index].index, sinks[sink_index].index)
