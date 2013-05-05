#include <Python.h>
#include "amlich.c"

static PyObject *
py_jd_from_date(PyObject *self, PyObject *args) {
	int dd, mm, yyyy;
	if (!PyArg_ParseTuple(args, "iii", &dd, &mm, &yyyy))
		return NULL;

	return Py_BuildValue("i", jd_from_date(dd, mm, yyyy));
}
static PyObject *
py_jd_to_date(PyObject *self, PyObject *args) {
	int jd;
	if (!PyArg_ParseTuple(args, "i", &jd))
		return NULL;

	solar_date *d = jd_to_date(jd);

	PyObject *date = Py_BuildValue("[iii]", d->day, d->month, d->year);
	free(d);
	return date;
}
static PyObject *
py_new_moon(PyObject *self, PyObject *args) {
	int k;
	if (!PyArg_ParseTuple(args, "i", &k))
		return NULL;

	return Py_BuildValue("d", new_moon(k));

}
static PyObject *
py_sun_longitude(PyObject *self, PyObject *args) {
	double jdn;

	if (!PyArg_ParseTuple(args, "d", &jdn))
		return NULL;

	return Py_BuildValue("d", sun_longitude(jdn));
}
static PyObject *
py_get_sun_longitude(PyObject *self, PyObject *args) {
	int jd, time_zone;

	if (!PyArg_ParseTuple(args, "ii", &jd, &time_zone))
		return NULL;

	return Py_BuildValue("i", get_sun_longitude(jd, time_zone));
}
static PyObject *
py_get_new_moon_day(PyObject *self, PyObject *args) {
	int k, time_zone;
	if (!PyArg_ParseTuple(args, "ii", &k, &time_zone))
		return NULL;

	return Py_BuildValue("i", get_new_moon_day(k, time_zone));
}
static PyObject *
py_get_lunar_month11(PyObject *self, PyObject *args) {
	int yyyy, time_zone;
	if (!PyArg_ParseTuple(args, "ii", &yyyy, &time_zone))
		return NULL;

	return Py_BuildValue("i", get_lunar_month11(yyyy, time_zone));
}
static PyObject *
py_get_leap_month_offset(PyObject *self, PyObject *args) {
	int a11, time_zone;

	if (!PyArg_ParseTuple(args, "ii", &a11, &time_zone))
		return NULL;

	return Py_BuildValue("i", get_leap_month_offset(a11, time_zone));
}

static PyObject *
py_solar2lunar(PyObject *self, PyObject *args) {
	int dd, mm, yyyy, time_zone;

	if (!PyArg_ParseTuple(args, "iiii", &dd, &mm, &yyyy, &time_zone))
		return NULL;

	lunar_date *d = solar2lunar(dd, mm, yyyy, time_zone);
	PyObject *list = Py_BuildValue("[iiii]", d->day, d->month, d->year, d->leap);
	free(d);
	return list;
}
static PyObject *
py_lunar2solar(PyObject *self, PyObject *args) {
	int lunar_day, lunar_month, lunar_year, lunar_leap, time_zone;

	if (!PyArg_ParseTuple(args, "iiiii", &lunar_day, &lunar_month, &lunar_year,
			&lunar_leap, &time_zone))
		return NULL;

	solar_date *d = lunar2solar(lunar_day, lunar_month, lunar_year, lunar_leap, time_zone);

	PyObject *list = Py_BuildValue("[iii]", d->day, d->month, d->year);
	free(d);
	return list;
}

static PyMethodDef
methods[] = {
	{"jd_from_date", py_jd_from_date, METH_VARARGS, "Lunar Calendar - jd_from_date" },
	{"jd_to_date", py_jd_to_date, METH_VARARGS, "Lunar Calendar - jd_to_date" },
	{"new_moon", py_new_moon, METH_VARARGS, "Lunar Calendar - new_moon" },
	{"sun_longitude", py_sun_longitude, METH_VARARGS,"Lunar Calendar - sun_longitude" },
	{"get_sun_longitude", py_get_sun_longitude, METH_VARARGS, "Lunar Calendar - get_sun_longitude" },
	{"get_new_moon_day", py_get_new_moon_day, METH_VARARGS, "Lunar Calendar - get_new_moon_day" },
	{"get_lunar_month11", py_get_lunar_month11, METH_VARARGS, "Lunar Calendar - get_lunar_month11" },
	{"get_leap_month_offset", py_get_leap_month_offset, METH_VARARGS, "Lunar Calendar - get_leap_month_offset" },
	{ "solar2lunar", py_solar2lunar, METH_VARARGS, "Lunar Calendar - solar2lunar" },
	{ "lunar2solar", py_lunar2solar, METH_VARARGS, "Lunar Calendar - lunar2solar" },
	{ NULL, NULL, 0, NULL }
};

PyMODINIT_FUNC initcamlich(void) {
	(void) Py_InitModule("camlich", methods);
}
