import unittest
from closest_pair import distance
from closest_pair import brute_force
from closest_pair import strip_closest
from closest_pair import closest_pair


# Clase de pruebas unitarias para el problema "Closest Pair of Points"
class TestClosestPair(unittest.TestCase):

    # Prueba la función de cálculo de distancia entre dos puntos
    def test_distance(self):
        # Distancia entre (0,0) y (3,4) debería ser 5 (3-4-5 triángulo)
        self.assertAlmostEqual(distance((0, 0), (3, 4)), 5.0)
        # Distancia entre (1,1) y (4,5) debería ser 5
        self.assertAlmostEqual(distance((1, 1), (4, 5)), 5.0)
        # Distancia entre (-1,-1) y (-4,-5) debería ser 5
        self.assertAlmostEqual(distance((-1, -1), (-4, -5)), 5.0)

    # Prueba la función brute_force para encontrar el par más cercano en pequeños conjuntos de puntos
    def test_brute_force(self):
        points = [(0, 0), (1, 1), (4, 5), (3, 4)]
        pair, dist = brute_force(points)
        expected_pair = ((0, 0), (1, 1))
        expected_dist = distance((0, 0), (1, 1))
        # Verifica que el par devuelto sea el esperado, independientemente del orden
        self.assertTrue(pair == expected_pair or pair == tuple(reversed(expected_pair)))
        # Verifica que la distancia calculada sea la correcta
        self.assertAlmostEqual(dist, expected_dist)

    # Prueba la función closest_pair en un caso más complejo con más puntos
    def test_closest_pair_complex(self):
        points = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
        pair, dist = closest_pair(points)
        expected_pair = ((2, 3), (3, 4))
        expected_dist = distance((2, 3), (3, 4))
        # Verifica que el par devuelto sea el esperado, independientemente del orden
        self.assertTrue(pair == expected_pair or pair == tuple(reversed(expected_pair)))
        # Verifica que la distancia calculada sea la correcta
        self.assertAlmostEqual(dist, expected_dist)

    # Prueba el manejo de puntos duplicados, lo que debería resultar en una distancia de 0
    def test_closest_pair_duplicates(self):
        points = [(1, 2), (1, 2), (3, 4), (5, 6)]
        pair, dist = closest_pair(points)
        expected_pair = ((1, 2), (1, 2))
        expected_dist = 0.0
        # Verifica que el par devuelto sea el duplicado y la distancia sea 0
        self.assertEqual(pair, expected_pair)
        self.assertEqual(dist, expected_dist)

    # Prueba el manejo de puntos idénticos, todos los puntos son iguales, la distancia debe ser 0
    def test_closest_pair_all_same(self):
        points = [(1, 1), (1, 1), (1, 1), (1, 1)]
        pair, dist = closest_pair(points)
        expected_pair = ((1, 1), (1, 1))
        expected_dist = 0.0
        # Verifica que el par devuelto sea idéntico y la distancia sea 0
        self.assertEqual(pair, expected_pair)
        self.assertEqual(dist, expected_dist)


# Ejecuta todas las pruebas definidas
if __name__ == "__main__":
    unittest.main()
