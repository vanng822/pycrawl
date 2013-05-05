#include <Python.h>
#include <stdio.h>

#define BAILOUT 16
#define MAX_ITERATIONS 1000

int _mandelbrot(double x, double y)
{
	double cr = y - 0.5;
	double ci = x;
	double zi = 0.0;
	double zr = 0.0;
	int i = 0;

	while(1) {
		i ++;
		double temp = zr * zi;
		double zr2 = zr * zr;
		double zi2 = zi * zi;
		zr = zr2 - zi2 + cr;
		zi = temp + temp + ci;
		if (zi2 + zr2 > BAILOUT)
			return i;
		if (i > MAX_ITERATIONS)
			return 0;
	}

}

static PyObject* mandelbrot(PyObject* self, PyObject* args) {
	int x,y;
	for (y = -39; y < 39; y++) {
		printf("\n");
		for (x = -39; x < 39; x++) {
			int i = _mandelbrot(x/40.0, y/40.0);
			if (i==0)
				printf("*");
			else
				printf(" ");
		}
	}
	printf ("\n");

    return Py_BuildValue("i", 0);
}

static PyMethodDef methods[] = {
    {"mandelbrot", mandelbrot, METH_VARARGS, "Fractal - Mandelbrot"},
    {NULL, NULL, 0, NULL}
};


PyMODINIT_FUNC
initcmandelbrot(void)
{
    (void) Py_InitModule("cmandelbrot", methods);
}
