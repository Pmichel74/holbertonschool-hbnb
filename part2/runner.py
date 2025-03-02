# runner.py
import unittest
import sys
import coverage

def run_tests():
    # Démarrer la couverture de code
    cov = coverage.Coverage()
    cov.start()

    # Découvrir et lancer tous les tests
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    
    # Configurer le runner avec une sortie détaillée
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Arrêter et sauvegarder la couverture
    cov.stop()
    cov.save()

    # Générer le rapport de couverture
    cov.report()
    # Optionnel : générer un rapport HTML
    cov.html_report(directory='coverage_report')

    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
