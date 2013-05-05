#include <Python.h>
#include "amlich.c"

static PyObject* py_jd_from_date(PyObject* self, PyObject* args) {
	int dd, mm, yy;

	return Py_BuildValue("i", jd_from_date(dd, mm, yy));
}
static PyObject* py_jd_to_date(PyObject* self, PyObject* args) {
	int jd;

	return Py_BuildValue("[items]", jd_to_date(jd));
}
static PyObject* py_newmoon(PyObject* self, PyObject* args) {
	int k;

	return Py_BuildValue("d", newmoon(k));

}
static PyObject* py_sun_longitude(PyObject* self, PyObject* args) {
	double jdn;

	return Py_BuildValue("d", sun_longitude(jdn));
}
static PyObject* py_get_sun_longitude(PyObject* self, PyObject* args) {
	int jd, time_zone;

	return Py_BuildValue("i", get_sun_longitude(jd, time_zone));
}
static PyObject* py_get_newmoon_day(PyObject* self, PyObject* args) {
	int k, time_zone;

	return Py_BuildValue("i", get_newmoon_day(k, time_zone));
}
static PyObject* py_get_lunar_month11(PyObject* self, PyObject* args) {
	int yyyy, time_zone;

	return Py_BuildValue("i", get_lunar_month11(yyyy, time_zone));
}
static PyObject* py_get_leap_month_offset(PyObject* self, PyObject* args) {
	int a11, time_zone;

	return Py_BuildValue("i", get_leap_month_offset(a11, time_zone));
}

static PyObject* py_solar2lunar(PyObject* self, PyObject* args) {
	int dd, mm, yyyy, time_zone;

	if (!PyArg_ParseTuple(args, "iiii", &dd, &mm, &yyyy, &time_zone))
		return NULL;

	int *r = solar2lunar(dd, mm, yyyy, time_zone);

	PyListObject *list;
	list = (PyListObject *) Py_BuildValue("[]");
	int i;
	PyObject *i_new;
	for (i = 0; i < 4; i++) {
		i_new = (PyObject *) Py_BuildValue("i", r[i]);
		PyList_Append(list, i_new);
	}
	free(r);
	return (PyObject *) list;
}
static PyObject* py_lunar2solar(PyObject* self, PyObject* args) {
	int lunar_day, lunar_month, lunar_year, lunar_leap, time_zone;

	if (!PyArg_ParseTuple(args, "iiiii", &lunar_day, &lunar_month, &lunar_year,
			&lunar_leap, &time_zone))
		return NULL;

	int *r = lunar2solar(lunar_day, lunar_month, lunar_year, lunar_leap, time_zone);

	PyListObject *list;
	list = (PyListObject *) Py_BuildValue("[]");
	int i;
	PyObject *i_new;
	for (i = 0; i < 3; i++) {
		i_new = (PyObject *) Py_BuildValue("i", r[i]);
		PyList_Append(list, i_new);
	}
	free(r);
	return (PyObject *) list;
}

static PyMethodDef methods[] = { { "jd_from_date", py_jd_from_date,
		METH_VARARGS, "Lunar Calendar - jd_from_date" }, { "jd_to_date",
		py_jd_to_date, METH_VARARGS, "Lunar Calendar - jd_to_date" }, {
		"newmoon", py_newmoon, METH_VARARGS, "Lunar Calendar - newmoon" }, {
		"sun_longitude", py_sun_longitude, METH_VARARGS,
		"Lunar Calendar - sun_longitude" },
		{ "get_sun_longitude", py_get_sun_longitude, METH_VARARGS,
				"Lunar Calendar - get_sun_longitude" }, { "get_newmoon_day",
				py_get_newmoon_day, METH_VARARGS,
				"Lunar Calendar - get_newmoon_day" }, { "get_lunar_month11",
				py_get_lunar_month11, METH_VARARGS,
				"Lunar Calendar - get_lunar_month11" }, {
				"get_leap_month_offset", py_get_leap_month_offset, METH_VARARGS,
				"Lunar Calendar - get_leap_month_offset" }, { "solar2lunar",
				py_solar2lunar, METH_VARARGS, "Lunar Calendar - solar2lunar" },
		{ "lunar2solar", py_lunar2solar, METH_VARARGS,
				"Lunar Calendar - lunar2solar" }, { NULL, NULL, 0, NULL } };

PyMODINIT_FUNC initcamlich(void) {
	(void) Py_InitModule("camlich", methods);
}
