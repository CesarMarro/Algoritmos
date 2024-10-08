import unittest
import numpy as np
from middle_square import middle_square


class TestMiddleSquare(unittest.TestCase):
    def test_correct_length(self):
        """
        Verifica que la función genere la cantidad correcta de números aleatorios.
        """
        n = 10
        seed = 1234
        result = middle_square(n, seed)
        self.assertEqual(len(result), n)

    def test_normalization(self):
        """
        Verifica que todos los números generados estén en el rango [0, 1).
        """
        n = 100
        seed = 5678
        result = middle_square(n, seed)
        self.assertTrue(np.all(result >= 0))
        self.assertTrue(np.all(result < 1))

    def test_deterministic_output(self):
        """
        Verifica que la función genere la misma secuencia de números para una semilla y n dados.
        """
        n = 5
        seed = 4321
        result1 = middle_square(n, seed)
        result2 = middle_square(n, seed)
        np.testing.assert_array_almost_equal(result1, result2)

    def test_seed_reinitialization(self):
        """
        Verifica que la función reinicie con la semilla original si el número generado es 0.
        """
        n = 5
        seed = 0  # Una semilla de 0 siempre producirá 0, que luego se reinicia a la semilla
        expected = np.array([0, 0, 0, 0, 0]) / 10000.0
        result = middle_square(n, seed)
        np.testing.assert_array_almost_equal(result, expected)

    def test_large_n(self):
        """
        Verifica que la función pueda manejar una secuencia grande sin errores.
        """
        n = 10000
        seed = 123456
        result = middle_square(n, seed)
        self.assertEqual(len(result), n)
        self.assertTrue(np.all(result >= 0))
        self.assertTrue(np.all(result < 1))

    def test_multiple_seeds(self):
        """
        Verifica que diferentes semillas produzcan diferentes secuencias.
        """
        n = 5
        seed1 = 1111
        seed2 = 2222
        result1 = middle_square(n, seed1)
        result2 = middle_square(n, seed2)
        # A menos que las secuencias coincidan por casualidad, deben ser diferentes
        with self.assertRaises(AssertionError):
            np.testing.assert_array_almost_equal(result1, result2)

    def test_zero_handling(self):
        """
        Verifica que cuando x se convierte en 0, la semilla original se reutiliza.
        """
        n = 3
        seed = 1000  # 1000^2 = 1000000, zfill(8) -> '01000000', extraer [2:6] -> '0000', x = 0 -> reinicia a seed
        expected = np.array([1000, 1000, 1000]) / 10000.0
        result = middle_square(n, seed)
        np.testing.assert_array_almost_equal(result, expected)


if __name__ == "__main__":
    unittest.main()
