#include <Python.h>
#include "date_util.c"


static PyObject* py_merge_interval(PyObject* self, PyObject* args)
{
    PyObject * intervals;
    PyObject * new_interval;
    int numLines;
    //interval_list *curr, * head;
    printf("CALLING %d\n", 1);

    // parse list object
    if (!PyArg_ParseTuple(args, "O!O", &PyList_Type, &intervals, &new_interval))
        return NULL;

    // get the length of the list
    numLines = PyList_Size(intervals);
    int i;
    //interval_list *dates = (interval_list *) malloc(sizeof(interval_list));
    //date *d;

    for (i = 0; i < numLines - 1; i++) {
    	//d = (date *) malloc(sizeof(date));
    	//PyObject *py_d = intervals[i];
    	//d->day = (int) PyDateTime_GET_DAY(py_d);
    	//int t = PyDate_Check((PyObject *) PyDict_GetItem((PyObject *) intervals[i], (PyObject *) "start_date"));
    	printf("%d\n", 1);
    }

    return Py_BuildValue("O", intervals);
}


static PyMethodDef dateutilMethods[] = {
    {"merge_interval", py_merge_interval, METH_VARARGS, "merging intervals"},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initdateutil(void)
{
    (void) Py_InitModule("dateutil", dateutilMethods);
}

