import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import resistor_decode as m


class Decodificar(unittest.TestCase):
    def test_casos_conocidos(self):
        casos = [
            (["rojo", "violeta", "marron", "oro"], 270, 5.0),
            (["marron", "negro", "rojo", "oro"], 1000, 5.0),
            (["amarillo", "violeta", "negro", "rojo", "marron"], 47000, 1.0),
        ]
        for bandas, valor, tol in casos:
            with self.subTest(bandas=bandas):
                self.assertEqual(m.decodificar(bandas), (valor, tol))

    def test_banda_invalida(self):
        with self.assertRaises(ValueError):
            m.decodificar(["rojo", "violeta", "turquesa", "oro"])

    def test_numero_de_bandas(self):
        with self.assertRaises(ValueError):
            m.decodificar(["rojo", "violeta", "oro"])


class Codificar(unittest.TestCase):
    def test_ida_y_vuelta(self):
        for ohmios in (47, 470, 1000, 2200, 47000):
            valor, tol = m.decodificar(m.codificar(ohmios))
            self.assertEqual(valor, ohmios)
            self.assertEqual(tol, 5.0)

    def test_valor_no_positivo(self):
        with self.assertRaises(ValueError):
            m.codificar(0)


class Formato(unittest.TestCase):
    def test_unidades(self):
        self.assertEqual(m.formatear(470), "470 Ω")
        self.assertEqual(m.formatear(4700), "4.7 kΩ")
        self.assertEqual(m.formatear(2_200_000), "2.2 MΩ")


if __name__ == "__main__":
    unittest.main()
