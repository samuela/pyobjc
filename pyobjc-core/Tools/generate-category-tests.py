#!/usr/bin/env python3
"""
Helper script that generates helpers for test cases that test
if PyObjC works properly in the presence of categories and related
dynamic features in Objective-C (e.g. method swifling).

Don't worry too much about formatting, the output will get
reformatted by black and clang-format.
"""
import pathlib
import textwrap
import itertools

TESTEXT_DIR = pathlib.Path(__file__).resolve().parent.parent / "Modules/objc/test"
TEST_DIR = pathlib.Path(__file__).resolve().parent.parent / "PyObjCTest"

EXT_PFX = """
/*
 *     *** GENERATED FILE ***
 *
 * This file is generated by Tools/generate-category-tests.py
 */
#include "Python.h"
#include "pyobjc-api.h"

#import <Foundation/Foundation.h>
"""

EXT_SFX = """
static PyMethodDef mod_methods[] = {{0, 0, 0, 0}};

static int mod_exec_module(PyObject* m)
{
    if (PyObjC_ImportAPI(m) < 0) {
        return -1;
    }
"""

EXT_END = """

    return 0;
}

static struct PyModuleDef_Slot mod_slots[] = {
    {
        .slot = Py_mod_exec,
        .value = (void*)mod_exec_module
    },
#if PY_VERSION_HEX >= 0x030c0000
    {
        /* This extension does not use the CPython API other than initializing
         * the module, hence is safe with subinterpreters and per-interpreter
         * GILs
         */
        .slot = Py_mod_multiple_interpreters,
        .value = Py_MOD_PER_INTERPRETER_GIL_SUPPORTED,
    },
#endif
#if PY_VERSION_HEX >= 0x030d0000
    {
        .slot = Py_mod_gil,
        .value = Py_MOD_GIL_NOT_USED,
    },
#endif
    {  /* Sentinel */
        .slot = 0,
        .value = 0
    }
};

static struct PyModuleDef mod_module = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "%(name)s",
    .m_doc = NULL,
    .m_size = 0,
    .m_methods = mod_methods,
    .m_slots = mod_slots,
    .m_traverse = NULL,
    .m_clear = NULL,
    .m_free = NULL,
};

PyObject* PyInit_%(name)s(void);

PyObject* __attribute__((__visibility__("default"))) _Nullable PyInit_%(name)s(void)
{
    return PyModuleDef_Init(&mod_module);
}
"""

BASE_TMPL = """

__attribute__((__visibility__("default")))
@interface OC_Category_GP%(idx)d : NSObject
{
}
-(id)gpMethod1; /* not overridden */
-(id)gpMethod2; /* overridden in P */
-(id)gpMethod3; /* overridden in P and C */
-(id)gpMethod4; /* overridden in C */
@end

__attribute__((__visibility__("default")))
@interface OC_Category_P%(idx)d : OC_Category_GP%(idx)d
{
}
-(id)gpMethod2;
-(id)gpMethod3;

-(id)pMethod1; /* not overridden */
-(id)pMethod2; /* overridden in C */
@end

__attribute__((__visibility__("default")))
@interface OC_Category_C%(idx)d : OC_Category_P%(idx)d
{
}
-(id)gpMethod3;
-(id)gpMethod4;
-(id)pMethod2;
-(id)method1;
@end

@implementation OC_Category_GP%(idx)d

-(id)gpMethod1 {
    return @"GP%(idx)d - method1 - GP";
}

-(id)gpMethod2 {
    return @"GP%(idx)d - method2 - GP";
}

-(id)gpMethod3 {
    return @"GP%(idx)d - method3 - GP";
}

-(id)gpMethod4 {
    return @"GP%(idx)d - method4 - GP";
}

@end

@implementation OC_Category_P%(idx)d

-(id)gpMethod2 {
    return @"GP%(idx)d - method2 - P";
}

-(id)gpMethod3 {
    return @"GP%(idx)d - method3 - P";
}

-(id)pMethod1 {
    return @"P%(idx)d - method1 - P";
}

-(id)pMethod2 {
    return @"P%(idx)d - method2 - P";
}

@end

@implementation OC_Category_C%(idx)d

-(id)gpMethod3 {
    return @"GP%(idx)d - method3 - C";
}

-(id)gpMethod4 {
    return @"GP%(idx)d - method4 - C";
}

-(id)pMethod2 {
    return @"P%(idx)d - method2 - C";
}

-(id)method1 {
    return @"C%(idx)d - method1 - C";
}

@end
"""

CAT_TMPL = """\
__attribute__((__visibility__("default")))
@interface OC_Category_GP%(idx)d : NSObject {}
@end

__attribute__((__visibility__("default")))
@interface OC_Category_P%(idx)d : OC_Category_GP%(idx)d {}
@end

__attribute__((__visibility__("default")))
@interface OC_Category_C%(idx)d : OC_Category_P%(idx)d {}
@end


@implementation OC_Category_%(class_id)s(Cat)
-(id)gpMethod1 {
    return @"%(class_id)s - gpMethod1 - %(identifier)s";
}
-(id)gpMethod5 {
    return @"%(class_id)s - gpMethod5 - %(identifier)s";
}
-(id)pMethod1 {
    return @"%(class_id)s - pMethod1 - %(identifier)s";
}
-(id)pMethod3 {
    return @"%(class_id)s - pMethod3 - %(identifier)s";
}
-(id)method1 {
    return @"%(class_id)s - method1 - %(identifier)s";
}
-(id)method2 {
    return @"%(class_id)s - method2 - %(identifier)s";
}
@end
"""


def generate_category(mod_name, idx, class_id, identifier):
    with open(TESTEXT_DIR / f"{mod_name}.m", "w") as stream:
        stream.write(EXT_PFX)
        stream.write(
            CAT_TMPL
            % {
                "class_id": class_id,
                "identifier": identifier,
                "idx": idx,
            }
        )
        stream.write(EXT_SFX)
        stream.write(EXT_END % {"name": mod_name})


def generate_testext_base(num_base):
    with open(TESTEXT_DIR / "categories_base.m", "w") as stream:
        stream.write(EXT_PFX)
        for idx in range(num_base):
            stream.write(BASE_TMPL % {"idx": idx})
        stream.write(EXT_SFX)
        for idx in range(num_base):
            stream.write(
                textwrap.dedent(
                    f"""\
                    if (PyModule_AddObject(m, "OC_Category_GP{idx}", PyObjC_IdToPython([OC_Category_GP{idx} class]))
                        < 0) {{
                        return -1;
                   }}
                    if (PyModule_AddObject(m, "OC_Category_P{idx}", PyObjC_IdToPython([OC_Category_P{idx} class]))
                        < 0) {{
                        return -1;
                    }}
                    if (PyModule_AddObject(m, "OC_Category_C{idx}", PyObjC_IdToPython([OC_Category_C{idx} class]))
                        < 0) {{
                        return -1;
                    }}
                    """
                )
            )

        stream.write(EXT_END % {"name": "categories_base"})


TESTCASE_PFX = """
'''
Tests for handling Objective-C categories that are loaded
in Objective-C.

These tests are primarily here to check that caching
of attribute lookups works correctly, even when
there are categories or other dynamic behaviours that
add to the set of methods on a class (directly or
indirectly).

     *** GENERATED FILE ***

These tests are generated from Tools/generate-category-tests.py
'''

from PyObjCTools.TestSupport import TestCase
from . import categories_base as mod

class TestCategories(TestCase):
"""

ORDER = ("grandparent", "parent", "child")


def generate_testcases() -> int:
    num_base = 0
    with open(TEST_DIR / "test_categories.py", "w") as stream:
        stream.write(TESTCASE_PFX)

        # All tests are done with all possible orders of
        # looking in child, parent and grandparent to ensure
        # caching doesn't mess things up.

        # Base case: Check attribute resolution when no
        #            categories are used
        for order in itertools.permutations(ORDER):
            stream.write(f"    def test_base_methods_{'_'.join(order)}(self):\n")
            for c in order:
                if c == "child":
                    stream.write(
                        f"""\
        with self.subTest("child"):
            o = mod.OC_Category_C{num_base}.alloc().init()
            self.assertEqual(o.gpMethod1(), "GP{num_base} - method1 - GP")
            self.assertEqual(o.gpMethod2(), "GP{num_base} - method2 - P")
            self.assertEqual(o.gpMethod3(), "GP{num_base} - method3 - C")
            self.assertEqual(o.gpMethod4(), "GP{num_base} - method4 - C")

            self.assertEqual(o.pMethod1(), "P{num_base} - method1 - P")
            self.assertEqual(o.pMethod2(), "P{num_base} - method2 - C")

            self.assertEqual(o.method1(), "C{num_base} - method1 - C")
         """
                    )
                stream.write("\n")

                if c == "parent":
                    stream.write(
                        f"""\
        with self.subTest("parent"):
            o = mod.OC_Category_P{num_base}.alloc().init()
            self.assertEqual(o.gpMethod1(), "GP{num_base} - method1 - GP")
            self.assertEqual(o.gpMethod2(), "GP{num_base} - method2 - P")
            self.assertEqual(o.gpMethod3(), "GP{num_base} - method3 - P")
            self.assertEqual(o.gpMethod4(), "GP{num_base} - method4 - GP")

            self.assertEqual(o.pMethod1(), "P{num_base} - method1 - P")
            self.assertEqual(o.pMethod2(), "P{num_base} - method2 - P")

         """
                    )
                stream.write("\n")

                if c == "parent":
                    stream.write(
                        f"""\
        with self.subTest("grandparent"):
            o = mod.OC_Category_GP{num_base}.alloc().init()
            self.assertEqual(o.gpMethod1(), "GP{num_base} - method1 - GP")
            self.assertEqual(o.gpMethod2(), "GP{num_base} - method2 - GP")
            self.assertEqual(o.gpMethod3(), "GP{num_base} - method3 - GP")
            self.assertEqual(o.gpMethod4(), "GP{num_base} - method4 - GP")

         """
                    )
                stream.write("\n")

            num_base += 1

        # Category on grandparent:
        # - override method in parent
        # - override method in grandparent
        # - 'override' method in class
        #
        # With an additional test axis w.r.t. when
        # the category is loaded:
        #    - Load category before instantiating
        #    - Load category before calling methods
        #    - First call methods, then load category, then check result

        for order in itertools.permutations(ORDER):
            for load in ("before_inst", "after_inst", "after_calls"):
                generate_category(
                    f"category_gp{num_base}",
                    num_base,
                    f"GP{num_base}",
                    f"GP{num_base}(Cat)",
                )
                stream.write(
                    f"    def  test_category_on_grandparent_{load}_{'_'.join(order)}(self):\n"
                )
                if load == "before_inst":
                    stream.write(
                        f"        from . import category_gp{num_base}   # noqa: F401\n"
                    )

                stream.write(
                    f"""\
        c = mod.OC_Category_C{num_base}.alloc().init()
        p = mod.OC_Category_P{num_base}.alloc().init()
        gp = mod.OC_Category_GP{num_base}.alloc().init()
        """
                )
                stream.write("\n")

                if load == "after_inst":
                    stream.write(
                        f"        from . import category_gp{num_base}   # noqa: F401\n"
                    )

                if load == "after_calls":
                    for i in ("c", "p", "gp"):
                        stream.write(f"        {i}.gpMethod1()\n")
                        stream.write(f"        {i}.gpMethod2()\n")
                        stream.write(f"        {i}.gpMethod3()\n")
                        stream.write(f"        {i}.gpMethod4()\n")
                        # stream.write(f"        {i}.gpMethod5()\n")

                    for i in ("c", "p"):
                        stream.write(f"        {i}.pMethod1()\n")
                        stream.write(f"        {i}.pMethod2()\n")
                        # stream.write(f"        {i}.pMethod3()\n")

                    stream.write("        c.method1()\n")
                    # stream.write("        c.method2()\n")
                    stream.write(
                        f"        from . import category_gp{num_base}   # noqa: F401\n"
                    )

                for c in order:
                    if c == "child":
                        stream.write(
                            f"""\
        with self.subTest("child"):
            self.assertEqual(c.gpMethod1(), "GP{num_base} - gpMethod1 - GP{num_base}(Cat)")
            self.assertEqual(c.gpMethod2(), "GP{num_base} - method2 - P")
            self.assertEqual(c.gpMethod3(), "GP{num_base} - method3 - C")
            self.assertEqual(c.gpMethod4(), "GP{num_base} - method4 - C")
            self.assertEqual(c.gpMethod5(), "GP{num_base} - gpMethod5 - GP{num_base}(Cat)")

            self.assertEqual(c.pMethod1(), "P{num_base} - method1 - P")
            self.assertEqual(c.pMethod2(), "P{num_base} - method2 - C")
            self.assertEqual(c.pMethod3(), "GP{num_base} - pMethod3 - GP{num_base}(Cat)")

            self.assertEqual(c.method1(), "C{num_base} - method1 - C")
            self.assertEqual(c.method2(), "GP{num_base} - method2 - GP{num_base}(Cat)")
         """
                        )
                        stream.write("\n")

                    if c == "parent":
                        stream.write(
                            f"""\
        with self.subTest("parent"):
            self.assertEqual(p.gpMethod1(), "GP{num_base} - gpMethod1 - GP{num_base}(Cat)")
            self.assertEqual(p.gpMethod2(), "GP{num_base} - method2 - P")
            self.assertEqual(p.gpMethod3(), "GP{num_base} - method3 - P")
            self.assertEqual(p.gpMethod4(), "GP{num_base} - method4 - GP")
            self.assertEqual(p.gpMethod5(), "GP{num_base} - gpMethod5 - GP{num_base}(Cat)")

            self.assertEqual(p.pMethod1(), "P{num_base} - method1 - P")
            self.assertEqual(p.pMethod2(), "P{num_base} - method2 - P")
            self.assertEqual(p.pMethod3(), "GP{num_base} - pMethod3 - GP{num_base}(Cat)")
         """
                        )
                        stream.write("\n")

                    if c == "grandparent":
                        stream.write(
                            f"""\
        with self.subTest("grandparent"):
            self.assertEqual(gp.gpMethod1(), "GP{num_base} - gpMethod1 - GP{num_base}(Cat)")
            self.assertEqual(gp.gpMethod2(), "GP{num_base} - method2 - GP")
            self.assertEqual(gp.gpMethod3(), "GP{num_base} - method3 - GP")
            self.assertEqual(gp.gpMethod4(), "GP{num_base} - method4 - GP")
            self.assertEqual(gp.gpMethod5(), "GP{num_base} - gpMethod5 - GP{num_base}(Cat)")
         """
                        )
                        stream.write("\n")

                num_base += 1

        # Category on parent:
        # - override method in parent
        # - override method in grandparent
        # - 'override' method in class
        #
        # With an additional test axis w.r.t. when
        # the category is loaded:
        #    - Load category before instantiating
        #    - Load category before calling methods
        #    - First call methods, then load category, then check result
        for order in itertools.permutations(ORDER):
            for load in ("before_inst", "after_inst", "after_calls"):
                generate_category(
                    f"category_p{num_base}",
                    num_base,
                    f"P{num_base}",
                    f"P{num_base}(Cat)",
                )
                stream.write(
                    f"    def  test_category_on_parent_{load}_{'_'.join(order)}(self):\n"
                )
                if load == "before_inst":
                    stream.write(
                        f"        from . import category_p{num_base}   # noqa: F401\n"
                    )

                stream.write(
                    f"""\
        c = mod.OC_Category_C{num_base}.alloc().init()
        p = mod.OC_Category_P{num_base}.alloc().init()
        gp = mod.OC_Category_GP{num_base}.alloc().init()
        """
                )
                stream.write("\n")

                if load == "after_inst":
                    stream.write(
                        f"        from . import category_p{num_base}   # noqa: F401\n"
                    )

                if load == "after_calls":
                    for i in ("c", "p", "gp"):
                        stream.write(f"        {i}.gpMethod1()\n")
                        stream.write(f"        {i}.gpMethod2()\n")
                        stream.write(f"        {i}.gpMethod3()\n")
                        stream.write(f"        {i}.gpMethod4()\n")
                        # stream.write(f"        {i}.gpMethod5()\n")

                    for i in ("c", "p"):
                        stream.write(f"        {i}.pMethod1()\n")
                        stream.write(f"        {i}.pMethod2()\n")
                        # stream.write(f"        {i}.pMethod3()\n")

                    stream.write("        c.method1()\n")
                    # stream.write("        c.method2()\n")
                    stream.write(
                        f"        from . import category_p{num_base}  # noqa: F401\n"
                    )

                for c in order:
                    if c == "child":
                        stream.write(
                            f"""\
        with self.subTest("child"):
            self.assertEqual(c.gpMethod1(), "P{num_base} - gpMethod1 - P{num_base}(Cat)")
            self.assertEqual(c.gpMethod2(), "GP{num_base} - method2 - P")
            self.assertEqual(c.gpMethod3(), "GP{num_base} - method3 - C")
            self.assertEqual(c.gpMethod4(), "GP{num_base} - method4 - C")
            self.assertEqual(c.gpMethod5(), "P{num_base} - gpMethod5 - P{num_base}(Cat)")

            self.assertEqual(c.pMethod1(), "P{num_base} - pMethod1 - P{num_base}(Cat)")
            self.assertEqual(c.pMethod2(), "P{num_base} - method2 - C")
            self.assertEqual(c.pMethod3(), "P{num_base} - pMethod3 - P{num_base}(Cat)")

            self.assertEqual(c.method1(), "C{num_base} - method1 - C")
            self.assertEqual(c.method2(), "P{num_base} - method2 - P{num_base}(Cat)")
         """
                        )
                        stream.write("\n")

                    if c == "parent":
                        stream.write(
                            f"""\
        with self.subTest("parent"):
            self.assertEqual(p.gpMethod1(), "P{num_base} - gpMethod1 - P{num_base}(Cat)")
            self.assertEqual(p.gpMethod2(), "GP{num_base} - method2 - P")
            self.assertEqual(p.gpMethod3(), "GP{num_base} - method3 - P")
            self.assertEqual(p.gpMethod4(), "GP{num_base} - method4 - GP")
            self.assertEqual(p.gpMethod5(), "P{num_base} - gpMethod5 - P{num_base}(Cat)")

            self.assertEqual(p.pMethod1(), "P{num_base} - pMethod1 - P{num_base}(Cat)")
            self.assertEqual(p.pMethod2(), "P{num_base} - method2 - P")
            self.assertEqual(p.pMethod3(), "P{num_base} - pMethod3 - P{num_base}(Cat)")
         """
                        )
                        stream.write("\n")

                    if c == "grandparent":
                        stream.write(
                            f"""\
        with self.subTest("grandparent"):
            self.assertEqual(gp.gpMethod1(), "GP{num_base} - method1 - GP")
            self.assertEqual(gp.gpMethod2(), "GP{num_base} - method2 - GP")
            self.assertEqual(gp.gpMethod3(), "GP{num_base} - method3 - GP")
            self.assertEqual(gp.gpMethod4(), "GP{num_base} - method4 - GP")
            #self.assertEqual(gp.gpMethod5(), "GP{num_base} - method5 - GP")
         """
                        )
                        stream.write("\n")

                num_base += 1

        # Category on child:
        # - override method in parent
        # - override method in grandparent
        # - 'override' method in class
        #
        # With an additional test axis w.r.t. when
        # the category is loaded:
        #    - Load category before instantiating
        #    - Load category before calling methods
        #    - First call methods, then load category, then check result
        for order in itertools.permutations(ORDER):
            for load in ("before_inst", "after_inst", "after_calls"):
                generate_category(
                    f"category_c{num_base}",
                    num_base,
                    f"C{num_base}",
                    f"C{num_base}(Cat)",
                )
                stream.write(
                    f"    def  test_category_on_child_{load}_{'_'.join(order)}(self):\n"
                )
                if load == "before_inst":
                    stream.write(
                        f"        from . import category_c{num_base}  # noqa: F401\n"
                    )

                stream.write(
                    f"""\
        c = mod.OC_Category_C{num_base}.alloc().init()
        p = mod.OC_Category_P{num_base}.alloc().init()
        gp = mod.OC_Category_GP{num_base}.alloc().init()
        """
                )
                stream.write("\n")

                if load == "after_inst":
                    stream.write(
                        f"        from . import category_c{num_base}  # noqa: F401\n"
                    )

                if load == "after_calls":
                    for i in ("c", "p", "gp"):
                        stream.write(f"        {i}.gpMethod1()\n")
                        stream.write(f"        {i}.gpMethod2()\n")
                        stream.write(f"        {i}.gpMethod3()\n")
                        stream.write(f"        {i}.gpMethod4()\n")
                        # stream.write(f"        {i}.gpMethod5()\n")

                    for i in ("c", "p"):
                        stream.write(f"        {i}.pMethod1()\n")
                        stream.write(f"        {i}.pMethod2()\n")
                        # stream.write(f"        {i}.pMethod3()\n")

                    stream.write("        c.method1()\n")
                    # stream.write("        c.method2()\n")
                    stream.write(
                        f"        from . import category_c{num_base}  # noqa: F401\n"
                    )

                for c in order:
                    if c == "child":
                        stream.write(
                            f"""\
        with self.subTest("child"):
            self.assertEqual(c.gpMethod1(), "C{num_base} - gpMethod1 - C{num_base}(Cat)")
            self.assertEqual(c.gpMethod2(), "GP{num_base} - method2 - P")
            self.assertEqual(c.gpMethod3(), "GP{num_base} - method3 - C")
            self.assertEqual(c.gpMethod4(), "GP{num_base} - method4 - C")
            self.assertEqual(c.gpMethod5(), "C{num_base} - gpMethod5 - C{num_base}(Cat)")

            self.assertEqual(c.pMethod1(), "C{num_base} - pMethod1 - C{num_base}(Cat)")
            self.assertEqual(c.pMethod2(), "P{num_base} - method2 - C")
            self.assertEqual(c.pMethod3(), "C{num_base} - pMethod3 - C{num_base}(Cat)")

            self.assertEqual(c.method1(), "C{num_base} - method1 - C{num_base}(Cat)")
            self.assertEqual(c.method2(), "C{num_base} - method2 - C{num_base}(Cat)")
         """
                        )
                        stream.write("\n")

                    if c == "parent":
                        stream.write(
                            f"""\
        with self.subTest("parent"):
            self.assertEqual(p.gpMethod1(), "GP{num_base} - method1 - GP")
            self.assertEqual(p.gpMethod2(), "GP{num_base} - method2 - P")
            self.assertEqual(p.gpMethod3(), "GP{num_base} - method3 - P")
            self.assertEqual(p.gpMethod4(), "GP{num_base} - method4 - GP")
            #self.assertEqual(p.gpMethod5(), "GP{num_base} - method5 - GP")

            self.assertEqual(p.pMethod1(), "P{num_base} - method1 - P")
            self.assertEqual(p.pMethod2(), "P{num_base} - method2 - P")
            #self.assertEqual(p.pMethod3(), "P{num_base} - method3 - P")
         """
                        )
                        stream.write("\n")

                    if c == "grandparent":
                        stream.write(
                            f"""\
        with self.subTest("grandparent"):
            self.assertEqual(gp.gpMethod1(), "GP{num_base} - method1 - GP")
            self.assertEqual(gp.gpMethod2(), "GP{num_base} - method2 - GP")
            self.assertEqual(gp.gpMethod3(), "GP{num_base} - method3 - GP")
            self.assertEqual(gp.gpMethod4(), "GP{num_base} - method4 - GP")
            #self.assertEqual(gp.gpMethod5(), "GP{num_base} - method5 - GP")
         """
                        )
                        stream.write("\n")

                num_base += 1

    return num_base


def main():
    num_base = generate_testcases()
    generate_testext_base(num_base)


if __name__ == "__main__":
    main()
