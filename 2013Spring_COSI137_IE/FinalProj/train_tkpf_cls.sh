#!/bin/sh

./svm-light-train.sh -t 5 -C + before_cls/bf_tkpf_feature.train before_cls/before_tkpf_cls.model
./svm-light-train.sh -t 5 -C + simul_cls/sm_tkpf_feature.train simul_cls/simul_tkpf_cls.model
./svm-light-train.sh -t 5 -C + modal_cls/md_tkpf_feature.train modal_cls/modal_tkpf_cls.model
./svm-light-train.sh -t 5 -C + evidential_cls/ed_tkpf_feature.train evidential_cls/evidential_tkpf_cls.model

./svm-light-test.sh event_tkpf_feature.test before_cls/before_tkpf_cls.model before_tkpf_cls.result
./svm-light-test.sh event_tkpf_feature.test simul_cls/simul_tkpf_cls.model simul_tkpf_cls.result
./svm-light-test.sh event_tkpf_feature.test modal_cls/modal_tkpf_cls.model modal_tkpf_cls.result
./svm-light-test.sh event_tkpf_feature.test evidential_cls/evidential_tkpf_cls.model evidential_tkpf_cls.result