#include <Python.h>

int main(void)
{
Py_Initialize();
PyRun_InteractiveLoop(stdin, "<stdin>");
Py_Finalize();
}