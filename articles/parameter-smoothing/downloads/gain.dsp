//---------------------------------------------------------
// Volume control in dB
// FAUST's own example: examples/SAM/volume/volume.dsp
// (c) GRAME, BSD license
//---------------------------------------------------------

import("stdfaust.lib");

gain    = vslider("Volume", 0, -70, +4, 0.1) : ba.db2linear : si.smoo;

process = _,_ : *(gain), *(gain);
