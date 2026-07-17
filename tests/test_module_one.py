import unittest

from tests.course_assertions import assert_module_contract


class ModuleOneTest(unittest.TestCase):
    def test_content(self):
        assert_module_contract(
            self,
            "modulo-1-visao-geral",
            (
                "componente",
                "conector",
                "atributo de qualidade",
                "camadas",
                "pipes and filters",
                "microkernel",
                "monólito modular",
                "ADR",
                "Structurizr Lite",
                "Python",
                ".NET",
                "Java",
            ),
        )


if __name__ == "__main__":
    unittest.main()
