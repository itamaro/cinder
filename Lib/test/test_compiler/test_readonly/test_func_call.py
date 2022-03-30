import unittest

from .common import ReadonlyTestBase


class FuncCallTests(ReadonlyTestBase):
    def test_call_nro_ro(self) -> None:
        code = """
        @readonly_func
        def g():
            return 1

        def f():
            return g()
        """
        with self.assertNoImmutableErrors():
            self._compile_and_run(code, "f")

    def test_call_ro_nro(self) -> None:
        code = """
        def g():
            return 1

        @readonly_func
        def f():
            return g()
        """
        with self.assertImmutableErrors(
            1, "A mutable function cannot be called in a readonly function."
        ):
            self._compile_and_run(code, "f")

    def test_call_ro_ro(self) -> None:
        code = """
        @readonly_func
        def g():
            return 1

        @readonly_func
        def f():
            return g()
        """
        with self.assertNoImmutableErrors():
            self._compile_and_run(code, "f")

    def test_returns_readonly_err(self) -> None:
        code = """
        @readonly_func
        def g() -> Readonly[int]:
            return 1

        @readonly_func
        def f():
            t = g()
            return t
        """
        with self.assertImmutableErrors(
            3, "Cannot assign a readonly value to a mutable variable."
        ):
            self._compile_and_run(code, "f")

    def test_no_returns_readonly_error(self) -> None:
        code = """
        @readonly_func
        def g() -> Readonly[int]:
            return 1

        @readonly_func
        def f():
            t: Readonly[int] = g()
            return t
        """
        with self.assertNoImmutableErrors():
            self._compile_and_run(code, "f")

    @unittest.skip("Argument readonly-ness is not correctly parsed yet.")
    def test_arguments(self) -> None:
        code = """
        @readonly_func
        def g(a, b: Readonly[int], c):
            return 1

        @readonly_func
        def f():
            t = g(1, 2, 3)
            return t
        """
        with self.assertImmutableErrors(4, ""):
            self._compile_and_run(code, "f")

    def test_readonly_closure_no_error(self) -> None:
        code = """
        def f():
            @readonly_func
            @readonly_closure
            def h():
                pass

            @readonly_func
            @readonly_closure
            def g():
                h()

            g()
        """
        with self.assertNoImmutableErrors():
            self._compile_and_run(code, "f")

    def test_readonly_closure_error(self) -> None:
        code = """
        def f():
            @readonly_func
            def i():
                pass

            @readonly_func
            @readonly_closure
            def g():
                i()

            g()
        """
        with self.assertImmutableErrors(
            2,
            "A function decorated with @readonly_closure cannot call another fuction without @readonly_closure decorated.",
        ):
            self._compile_and_run(code, "f")

    def _compile_and_run(self, code: str, func: str) -> None:
        f = self.compile_and_run(code)[func]
        return f()