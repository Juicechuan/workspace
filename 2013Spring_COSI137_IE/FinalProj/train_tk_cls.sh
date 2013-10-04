#!/bin/sh

./svm-light-train.sh -t 5 before_cls/bf_tk_feature.train before_cls/before_cls.model
./svm-light-train.sh -t 5 simul_cls/sm_tk_feature.train simul_cls/simul_cls.model
./svm-light-train.sh -t 5 modal_cls/md_tk_feature.train modal_cls/modal_cls.model
./svm-light-train.sh -t 5 evidential_cls/ed_tk_feature.train evidential_cls/evidential_cls.model

./svm-light-test.sh event_tk_feature.test before_cls/before_cls.model before_cls.result
./svm-light-test.sh event_tk_feature.test simul_cls/simul_cls.model simul_cls.result
./svm-light-test.sh event_tk_feature.test modal_cls/modal_cls.model modal_cls.result
./svm-light-test.sh event_tk_feature.test evidential_cls/evidential_cls.model evidential_cls.result