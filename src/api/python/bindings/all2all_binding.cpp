#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "ascend_ops/all2all.h"

namespace py = pybind11;

PYBIND11_MODULE(ascend_ops, m) {
    m.doc() = "AscendOps Python bindings"; 

    py::class_<ascend::ops::All2AllOp>(m, "All2AllOp")
        .def(py::init<>())
        .def("init", &ascend::ops::All2AllOp::Init,
             "Initialize the All2All operator",
             py::arg("shape"),
             py::arg("rank_ids"),
             py::arg("dtype"))
        .def("execute", &ascend::ops::All2AllOp::Execute,
             "Execute the All2All operator",
             py::arg("input"),
             py::arg("output"),
             py::arg("stream"));
} 