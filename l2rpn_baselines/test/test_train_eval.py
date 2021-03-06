# Copyright (c) 2020, RTE (https://www.rte-france.com)
# See AUTHORS.txt
# This Source Code Form is subject to the terms of the Mozilla Public License, version 2.0.
# If a copy of the Mozilla Public License, version 2.0 was not distributed with this file,
# you can obtain one at http://mozilla.org/MPL/2.0/.
# SPDX-License-Identifier: MPL-2.0
# This file is part of L2RPN Baselines, L2RPN Baselines a repository to host baselines for l2rpn competitions.

# test that the baselines can be imported
import os
import unittest
import warnings
import tempfile
import logging

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('tensorflow').setLevel(logging.FATAL)

import grid2op

from l2rpn_baselines.utils import TrainingParam, NNParam, make_multi_env
from l2rpn_baselines.DeepQSimple import train as train_dqn
from l2rpn_baselines.DeepQSimple import evaluate as eval_dqn
from l2rpn_baselines.DuelQSimple import train as train_d3qs
from l2rpn_baselines.DuelQSimple import evaluate as eval_d3qs
from l2rpn_baselines.SAC import train as train_sac
from l2rpn_baselines.SAC import evaluate as eval_sac
from l2rpn_baselines.DuelQLeapNet import train as train_leap
from l2rpn_baselines.DuelQLeapNet import evaluate as eval_leap
from l2rpn_baselines.DoubleDuelingDQN import train as train_d3qn
from l2rpn_baselines.DoubleDuelingDQN import evaluate as eval_d3qn
from l2rpn_baselines.DoubleDuelingDQN import DoubleDuelingDQNConfig as d3qn_cfg
from l2rpn_baselines.DoubleDuelingRDQN import train as train_rqn
from l2rpn_baselines.DoubleDuelingRDQN import evaluate as eval_rqn
from l2rpn_baselines.DoubleDuelingRDQN import DoubleDuelingRDQNConfig as rdqn_cfg
from l2rpn_baselines.SliceRDQN import train as train_srqn
from l2rpn_baselines.SliceRDQN import evaluate as eval_srqn
from l2rpn_baselines.SliceRDQN import SliceRDQN_Config as srdqn_cfg


class TestDeepQSimple(unittest.TestCase):
    def test_train_eval(self):
        tp = TrainingParam()
        tp.buffer_size = 100
        tp.minibatch_size = 8
        tp.update_freq = 32
        tp.min_observation = 32
        tmp_dir = tempfile.mkdtemp()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            env = grid2op.make("rte_case5_example", test=True)
            li_attr_obs_X = ["prod_p", "load_p", "rho"]

            # neural network architecture
            observation_size = NNParam.get_obs_size(env, li_attr_obs_X)
            sizes = [100, 50, 10]  # sizes of each hidden layers
            kwargs_archi = {'observation_size': observation_size,
                            'sizes': sizes,
                            'activs': ["relu" for _ in sizes],  # all relu activation function
                            "list_attr_obs": li_attr_obs_X}

            kwargs_converters = {"all_actions": None,
                                 "set_line_status": False,
                                 "change_bus_vect": True,
                                 "set_topo_vect": False
                                 }
            nm_ = "AnneOnymous"
            train_dqn(env,
                      name=nm_,
                      iterations=100,
                      save_path=tmp_dir,
                      load_path=None,
                      logs_dir=tmp_dir,
                      training_param=tp,
                      verbose=False,
                      kwargs_converters=kwargs_converters,
                      kwargs_archi=kwargs_archi)

            baseline_2 = eval_dqn(env,
                                  name=nm_,
                                  load_path=tmp_dir,
                                  logs_path=tmp_dir,
                                  nb_episode=1,
                                  nb_process=1,
                                  max_steps=30,
                                  verbose=False,
                                  save_gif=False)

    def test_train_eval_multi(self):
        tp = TrainingParam()
        tp.buffer_size = 100
        tp.minibatch_size = 8
        tp.update_freq = 32
        tp.min_observation = 32
        tmp_dir = tempfile.mkdtemp()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            env_init = grid2op.make("rte_case5_example", test=True)
            env = make_multi_env(env_init, 2)

            li_attr_obs_X = ["prod_p", "load_p", "rho"]

            # neural network architecture
            observation_size = NNParam.get_obs_size(env, li_attr_obs_X)
            sizes = [100, 50, 10]  # sizes of each hidden layers
            kwargs_archi = {'observation_size': observation_size,
                            'sizes': sizes,
                            'activs': ["relu" for _ in sizes],  # all relu activation function
                            "list_attr_obs": li_attr_obs_X}

            kwargs_converters = {"all_actions": None,
                                 "set_line_status": False,
                                 "change_bus_vect": True,
                                 "set_topo_vect": False
                                 }
            nm_ = "AnneOnymous"
            train_dqn(env,
                      name=nm_,
                      iterations=100,
                      save_path=tmp_dir,
                      load_path=None,
                      logs_dir=tmp_dir,
                      training_param=tp,
                      verbose=False,
                      kwargs_converters=kwargs_converters,
                      kwargs_archi=kwargs_archi)

            baseline_2 = eval_dqn(env_init,
                                  name=nm_,
                                  load_path=tmp_dir,
                                  logs_path=tmp_dir,
                                  nb_episode=1,
                                  nb_process=1,
                                  max_steps=30,
                                  verbose=False,
                                  save_gif=False)

class TestDuelQSimple(unittest.TestCase):
    def test_train_eval(self):
        tp = TrainingParam()
        tp.buffer_size = 100
        tp.minibatch_size = 8
        tp.update_freq = 32
        tp.min_observation = 32
        tmp_dir = tempfile.mkdtemp()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            env = grid2op.make("rte_case5_example", test=True)
            li_attr_obs_X = ["prod_p", "load_p", "rho"]

            # neural network architecture
            observation_size = NNParam.get_obs_size(env, li_attr_obs_X)
            sizes = [100, 50, 10]  # sizes of each hidden layers
            kwargs_archi = {'observation_size': observation_size,
                            'sizes': sizes,
                            'activs': ["relu" for _ in sizes],  # all relu activation function
                            "list_attr_obs": li_attr_obs_X}

            kwargs_converters = {"all_actions": None,
                                 "set_line_status": False,
                                 "change_bus_vect": True,
                                 "set_topo_vect": False
                                 }
            nm_ = "AnneOnymous"
            train_d3qs(env,
                      name=nm_,
                      iterations=100,
                      save_path=tmp_dir,
                      load_path=None,
                      logs_dir=tmp_dir,
                      training_param=tp,
                      verbose=False,
                      kwargs_converters=kwargs_converters,
                      kwargs_archi=kwargs_archi)

            baseline_2 = eval_d3qs(env,
                                  name=nm_,
                                  load_path=tmp_dir,
                                  logs_path=tmp_dir,
                                  nb_episode=1,
                                  nb_process=1,
                                  max_steps=30,
                                  verbose=False,
                                  save_gif=False)


class TestSAC(unittest.TestCase):
    def test_train_eval(self):
        tp = TrainingParam()
        tp.buffer_size = 100
        tp.minibatch_size = 8
        tp.update_freq = 32
        tp.min_observation = 32
        tmp_dir = tempfile.mkdtemp()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            env = grid2op.make("rte_case5_example", test=True)
            li_attr_obs_X = ["prod_p", "load_p", "rho"]

            # neural network architecture
            observation_size = NNParam.get_obs_size(env, li_attr_obs_X)
            sizes_q = [100, 50, 10]  # sizes of each hidden layers
            sizes_v = [100, 100]  # sizes of each hidden layers
            sizes_pol = [100, 10]  # sizes of each hidden layers
            kwargs_archi = {'observation_size': observation_size,
                            'sizes': sizes_q,
                            'activs': ["relu" for _ in range(len(sizes_q))],
                            "list_attr_obs": li_attr_obs_X,
                            "sizes_value": sizes_v,
                            "activs_value": ["relu" for _ in range(len(sizes_v))],
                            "sizes_policy": sizes_pol,
                            "activs_policy": ["relu" for _ in range(len(sizes_pol))]
                            }

            kwargs_converters = {"all_actions": None,
                                 "set_line_status": False,
                                 "change_bus_vect": True,
                                 "set_topo_vect": False
                                 }
            nm_ = "AnneOnymous"
            train_sac(env,
                      name=nm_,
                      iterations=100,
                      save_path=tmp_dir,
                      load_path=None,
                      logs_dir=tmp_dir,
                      training_param=tp,
                      verbose=False,
                      kwargs_converters=kwargs_converters,
                      kwargs_archi=kwargs_archi)

            baseline_2 = eval_sac(env,
                                  name=nm_,
                                  load_path=tmp_dir,
                                  logs_path=tmp_dir,
                                  nb_episode=1,
                                  nb_process=1,
                                  max_steps=30,
                                  verbose=False,
                                  save_gif=False)


class TestLeapNet(unittest.TestCase):
    def test_train_eval(self):
        tp = TrainingParam()
        tp.buffer_size = 100
        tp.minibatch_size = 8
        tp.update_freq = 32
        tp.min_observation = 32
        tmp_dir = tempfile.mkdtemp()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            env = grid2op.make("rte_case5_example", test=True)
            # neural network architecture
            li_attr_obs_X = ["prod_p", "load_p", "rho"]
            li_attr_obs_Tau = ["line_status"]
            sizes = [100, 50, 10]

            x_dim = NNParam.get_obs_size(env, li_attr_obs_X)
            tau_dims = [NNParam.get_obs_size(env, [el]) for el in li_attr_obs_Tau]

            kwargs_archi = {'sizes': sizes,
                            'activs': ["relu" for _ in sizes],
                            'x_dim': x_dim,
                            'tau_dims': tau_dims,
                            'tau_adds': [0.0 for _ in range(len(tau_dims))],
                            'tau_mults': [1.0 for _ in range(len(tau_dims))],
                            "list_attr_obs": li_attr_obs_X,
                            "list_attr_obs_tau": li_attr_obs_Tau
                            }

            kwargs_converters = {"all_actions": None,
                                 "set_line_status": False,
                                 "change_bus_vect": True,
                                 "set_topo_vect": False
                                 }
            nm_ = "AnneOnymous"
            train_leap(env,
                       name=nm_,
                       iterations=100,
                       save_path=tmp_dir,
                       load_path=None,
                       logs_dir=tmp_dir,
                       training_param=tp,
                       verbose=False,
                       kwargs_converters=kwargs_converters,
                       kwargs_archi=kwargs_archi)

            baseline_2 = eval_leap(env,
                                   name=nm_,
                                   load_path=tmp_dir,
                                   logs_path=tmp_dir,
                                   nb_episode=1,
                                   nb_process=1,
                                   max_steps=30,
                                   verbose=False,
                                   save_gif=False)


class TestD3QN(unittest.TestCase):
    def test_train_eval(self):
        tmp_dir = tempfile.mkdtemp()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            env = grid2op.make("rte_case5_example", test=True)
            nm_ = "test_D3QN"

            d3qn_cfg.INITIAL_EPISLON = 1.0
            d3qn_cfg.FINAL_EPISLON = 0.01
            d3qn_cfg.EPISLON_DECAY = 20
            d3qn_cfg.UPDATE_FREQ = 16
            
            train_d3qn(env,
                       name=nm_,
                       iterations=100,
                       save_path=tmp_dir,
                       load_path=None,
                       logs_path=tmp_dir,
                       learning_rate=1e-4,
                       verbose=False,
                       num_pre_training_steps=32,
                       num_frames=4,
                       batch_size=8)

            model_path = os.path.join(tmp_dir, nm_ + ".h5")
            eval_res = eval_d3qn(env,
                                 load_path=model_path,
                                 logs_path=tmp_dir,
                                 nb_episode=1,
                                 nb_process=1,
                                 max_steps=10,
                                 verbose=False,
                                 save_gif=False)

            assert eval_res is not None


class TestRDQN(unittest.TestCase):
    def test_train_eval(self):
        tmp_dir = tempfile.mkdtemp()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            env = grid2op.make("rte_case5_example", test=True)
            nm_ = "test_RDQN"
            rdqn_cfg.INITIAL_EPISLON = 1.0
            rdqn_cfg.FINAL_EPISLON = 0.01
            rdqn_cfg.EPISLON_DECAY = 20
            rdqn_cfg.UPDATE_FREQ = 16

            train_rqn(env,
                      name=nm_,
                      iterations=100,
                      save_path=tmp_dir,
                      load_path=None,
                      logs_path=tmp_dir,
                      learning_rate=1e-4,
                      verbose=False,
                      num_pre_training_steps=16,
                      batch_size=8)

            model_path = os.path.join(tmp_dir, nm_ + ".tf")
            eval_res = eval_rqn(env,
                                load_path=model_path,
                                logs_path=tmp_dir,
                                nb_episode=1,
                                nb_process=1,
                                max_steps=10,
                                verbose=False,
                                save_gif=False)

            assert eval_res is not None


class TestSRDQN(unittest.TestCase):
    def test_train_eval(self):
        tmp_dir = tempfile.mkdtemp()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            env = grid2op.make("rte_case5_example", test=True)
            nm_ = "test_SRDQN"
            srdqn_cfg.INITIAL_EPISLON = 1.0
            srdqn_cfg.FINAL_EPISLON = 0.01
            srdqn_cfg.EPISLON_DECAY = 20
            srdqn_cfg.UPDATE_FREQ = 16

            train_srqn(env,
                       name=nm_,
                       iterations=100,
                       save_path=tmp_dir,
                       load_path=None,
                       logs_path=tmp_dir,
                       learning_rate=1e-4,
                       verbose=False,
                       num_pre_training_steps=32,
                       batch_size=8)

            model_path = os.path.join(tmp_dir, nm_ + ".tf")
            eval_res = eval_srqn(env,
                                 load_path=model_path,
                                 logs_path=tmp_dir,
                                 nb_episode=1,
                                 nb_process=1,
                                 max_steps=10,
                                 verbose=False,
                                 save_gif=False)

            assert eval_res is not None


if __name__ == "__main__":
    unittest.main()
