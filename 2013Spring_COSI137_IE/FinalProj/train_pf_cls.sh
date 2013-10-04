#!/bin/sh

./svm-light-train.sh -t 5 -C V before_cls/bf_tkpf_feature.train before_cls/before_pf_cls.model
./svm-light-train.sh -t 5 -C V simul_cls/sm_tkpf_feature.train simul_cls/simul_pf_cls.model
./svm-light-train.sh -t 5 -C V modal_cls/md_tkpf_feature.train modal_cls/modal_pf_cls.model
./svm-light-train.sh -t 5 -C V evidential_cls/ed_tkpf_feature.train evidential_cls/evidential_pf_cls.model

./svm-light-test.sh event_tkpf_feature.test before_cls/before_pf_cls.model before_pf_cls.result
./svm-light-test.sh event_tkpf_feature.test simul_cls/simul_pf_cls.model simul_pf_cls.result
./svm-light-test.sh event_tkpf_feature.test modal_cls/modal_pf_cls.model modal_pf_cls.result
./svm-light-test.sh event_tkpf_feature.test evidential_cls/evidential_pf_cls.model evidential_pf_cls.result