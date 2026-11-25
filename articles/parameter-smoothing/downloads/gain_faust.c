/* ------------------------------------------------------------
name: "gain"
Code generated with Faust 2.37.3 (https://faust.grame.fr)
Compilation options: -lang c -es 1 -single -ftz 0
------------------------------------------------------------ */

#ifndef  __mydsp_H__
#define  __mydsp_H__

#ifndef FAUSTFLOAT
#define FAUSTFLOAT float
#endif 


#ifdef __cplusplus
extern "C" {
#endif

#include <math.h>
#include <stdint.h>
#include <stdlib.h>


#ifndef FAUSTCLASS 
#define FAUSTCLASS mydsp
#endif
#ifdef __APPLE__ 
#define exp10f __exp10f
#define exp10 __exp10
#endif

typedef struct {
	int fSampleRate;
	float fConst0;
	FAUSTFLOAT fVslider0;
	float fConst1;
	float fRec0[2];
} mydsp;

mydsp* newmydsp() { 
	mydsp* dsp = (mydsp*)calloc(1, sizeof(mydsp));
	return dsp;
}

void deletemydsp(mydsp* dsp) { 
	free(dsp);
}

void metadatamydsp(MetaGlue* m) { 
	m->declare(m->metaInterface, "basics.lib/name", "Faust Basic Element Library");
	m->declare(m->metaInterface, "basics.lib/version", "0.2");
	m->declare(m->metaInterface, "compile_options", "-lang c -es 1 -single -ftz 0");
	m->declare(m->metaInterface, "filename", "gain.dsp");
	m->declare(m->metaInterface, "maths.lib/author", "GRAME");
	m->declare(m->metaInterface, "maths.lib/copyright", "GRAME");
	m->declare(m->metaInterface, "maths.lib/license", "LGPL with exception");
	m->declare(m->metaInterface, "maths.lib/name", "Faust Math Library");
	m->declare(m->metaInterface, "maths.lib/version", "2.5");
	m->declare(m->metaInterface, "name", "gain");
	m->declare(m->metaInterface, "platform.lib/name", "Generic Platform Library");
	m->declare(m->metaInterface, "platform.lib/version", "0.2");
	m->declare(m->metaInterface, "signals.lib/name", "Faust Signal Routing Library");
	m->declare(m->metaInterface, "signals.lib/version", "0.1");
}

int getSampleRatemydsp(mydsp* dsp) {
	return dsp->fSampleRate;
}

int getNumInputsmydsp(mydsp* dsp) {
	return 2;
}
int getNumOutputsmydsp(mydsp* dsp) {
	return 2;
}

void classInitmydsp(int sample_rate) {
}

void instanceResetUserInterfacemydsp(mydsp* dsp) {
	dsp->fVslider0 = (FAUSTFLOAT)0.0f;
}

void instanceClearmydsp(mydsp* dsp) {
	/* C99 loop */
	{
		int l0;
		for (l0 = 0; (l0 < 2); l0 = (l0 + 1)) {
			dsp->fRec0[l0] = 0.0f;
		}
	}
}

void instanceConstantsmydsp(mydsp* dsp, int sample_rate) {
	dsp->fSampleRate = sample_rate;
	dsp->fConst0 = (44.0999985f / fminf(192000.0f, fmaxf(1.0f, (float)dsp->fSampleRate)));
	dsp->fConst1 = (1.0f - dsp->fConst0);
}

void instanceInitmydsp(mydsp* dsp, int sample_rate) {
	instanceConstantsmydsp(dsp, sample_rate);
	instanceResetUserInterfacemydsp(dsp);
	instanceClearmydsp(dsp);
}

void initmydsp(mydsp* dsp, int sample_rate) {
	classInitmydsp(sample_rate);
	instanceInitmydsp(dsp, sample_rate);
}

void buildUserInterfacemydsp(mydsp* dsp, UIGlue* ui_interface) {
	ui_interface->openVerticalBox(ui_interface->uiInterface, "gain");
	ui_interface->addVerticalSlider(ui_interface->uiInterface, "Volume", &dsp->fVslider0, (FAUSTFLOAT)0.0f, (FAUSTFLOAT)-70.0f, (FAUSTFLOAT)4.0f, (FAUSTFLOAT)0.100000001f);
	ui_interface->closeBox(ui_interface->uiInterface);
}

void computemydsp(mydsp* dsp, int count, FAUSTFLOAT** inputs, FAUSTFLOAT** outputs) {
	FAUSTFLOAT* input0 = inputs[0];
	FAUSTFLOAT* input1 = inputs[1];
	FAUSTFLOAT* output0 = outputs[0];
	FAUSTFLOAT* output1 = outputs[1];
	float fSlow0 = (dsp->fConst0 * powf(10.0f, (0.0500000007f * (float)dsp->fVslider0)));
	/* C99 loop */
	{
		int i0;
		for (i0 = 0; (i0 < count); i0 = (i0 + 1)) {
			dsp->fRec0[0] = (fSlow0 + (dsp->fConst1 * dsp->fRec0[1]));
			output0[i0] = (FAUSTFLOAT)((float)input0[i0] * dsp->fRec0[0]);
			output1[i0] = (FAUSTFLOAT)((float)input1[i0] * dsp->fRec0[0]);
			dsp->fRec0[1] = dsp->fRec0[0];
		}
	}
}

#ifdef __cplusplus
}
#endif

#endif
