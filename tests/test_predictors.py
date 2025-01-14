"""
Copyright (c) 2018 Manuel Peuster
ALL RIGHTS RESERVED.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Manuel Peuster, Paderborn University, manuel@peuster.de
"""
import unittest
from nfvtcp.predictor import PolynomialRegressionPredictor
from nfvtcp.predictor import SupportVectorRegressionPredictor
from nfvtcp.predictor import SVRPredictorRbfKernel
from nfvtcp.predictor import SVRPredictorLinearKernel
from nfvtcp.predictor import SVRPredictorPolyKernel
from nfvtcp.predictor import DecisionTreeRegressionPredictor
from nfvtcp.predictor import LassoRegressionPredictor
from nfvtcp.predictor import LassoLARSRegressionPredictor
from nfvtcp.predictor import ElasticNetRegressionPredictor
from nfvtcp.predictor import RidgeRegressionPredictor
from nfvtcp.predictor import SGDRegressionPredictor


class TestGenericPredictor(unittest.TestCase):
    """
    Iterate over predictor classes and to generic tests.
    """
    def setUp(self):
        # from http://scikit-learn.org/stable/modules/svm.html#svm-regression
        self.C_TRAIN = [[0.0, 0.0], [2.0, 2.0]]
        self.R_TRAIN = [0.5, 2.5]
        self.C_PREDICT = [[1.0, 1.0]]
        self.PREDICTORS = [PolynomialRegressionPredictor,
                           SupportVectorRegressionPredictor,
                           SVRPredictorRbfKernel,
                           SVRPredictorLinearKernel,
                           SVRPredictorPolyKernel,
                           DecisionTreeRegressionPredictor,
                           LassoRegressionPredictor,
                           LassoLARSRegressionPredictor,
                           ElasticNetRegressionPredictor,
                           RidgeRegressionPredictor,
                           SGDRegressionPredictor]

    def tearDown(self):
        pass

    def test_initialize(self):
        for p_cls in self.PREDICTORS:
            p = p_cls.generate({})[0]
            del p

    def test_train(self):
        for p_cls in self.PREDICTORS:
            p = p_cls.generate({})[0]
            p.train(self.C_TRAIN, self.R_TRAIN)

    def test_predict(self):
        for p_cls in self.PREDICTORS:
            p = p_cls.generate({})[0]
            p.train(self.C_TRAIN, self.R_TRAIN)
            r = p.predict(self.C_PREDICT)
            self.assertEqual(len(r), len(self.C_PREDICT))
            self.assertNotEqual(sum(r), 0.0)

    def test_reinitialize(self):
        for p_cls in self.PREDICTORS:
            p = p_cls.generate({})[0]
            p.reinitialize(0)

    def test_get_results(self):
        for p_cls in self.PREDICTORS:
            p = p_cls.generate({})[0]
            r = p.get_results()
            self.assertEqual(r.get("predictor"), p.short_name)


class TestPolyRegressionPredictor(unittest.TestCase):
    def setUp(self):
        self.C_TRAIN = [[0.0, 0.0], [2.0, 2.0]]
        self.R_TRAIN = [0.5, 2.5]
        self.C_PREDICT = [[1.0, 1.0]]

    def tearDown(self):
        pass

    def test_initialize(self):
        p = PolynomialRegressionPredictor.generate({})[0]
        del p

    def test_train(self):
        p = PolynomialRegressionPredictor.generate({})[0]
        p.train(self.C_TRAIN, self.R_TRAIN)

    def test_predict(self):
        p = PolynomialRegressionPredictor.generate({})[0]
        p.train(self.C_TRAIN, self.R_TRAIN)
        r = p.predict(self.C_PREDICT)
        if p.params.get("scale_x"):
            self.assertAlmostEqual(r[0], 0.5)
        else:
            self.assertAlmostEqual(r[0], 1.07142857)

    def test_reinitialize(self):
        p = PolynomialRegressionPredictor.generate({})[0]
        p.reinitialize(0)

    def test_get_results(self):
        p = PolynomialRegressionPredictor.generate({})[0]
        r = p.get_results()
        self.assertEqual(r.get("predictor"), "PRP")
        self.assertEqual(r.get("degree"), 2)
        self.assertEqual(r.get("epsilon"), 0.1)


class TestSupportVectorRegressionPredictor(unittest.TestCase):
    def setUp(self):
        # from http://scikit-learn.org/stable/modules/svm.html#svm-regression
        self.C_TRAIN = [[0.0, 0.0], [2.0, 2.0]]
        self.R_TRAIN = [0.5, 2.5]
        self.C_PREDICT = [[1.0, 1.0]]

    def tearDown(self):
        pass

    def test_initialize(self):
        p = SupportVectorRegressionPredictor.generate({})[0]
        del p

    def test_train(self):
        p = SupportVectorRegressionPredictor.generate({})[0]
        p.train(self.C_TRAIN, self.R_TRAIN)

    def test_predict(self):
        p = SupportVectorRegressionPredictor.generate({})[0]
        p.train(self.C_TRAIN, self.R_TRAIN)
        r = p.predict(self.C_PREDICT)
        if p.params.get("scale_x"):
            self.assertAlmostEqual(r[0], 0.8678794411)
        else:
            self.assertAlmostEqual(r[0], 1.5)

    def test_reinitialize(self):
        p = SupportVectorRegressionPredictor.generate({})[0]
        p.reinitialize(0)

    def test_get_results(self):
        p = SupportVectorRegressionPredictor.generate({})[0]
        r = p.get_results()
        self.assertEqual(r.get("predictor"), "SVRP")
        self.assertEqual(r.get("degree"), 2)
        self.assertEqual(r.get("epsilon"), 0.1)
