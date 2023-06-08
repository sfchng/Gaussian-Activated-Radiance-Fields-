import numpy as np
import os,sys
import torch
import importlib

import options
from util import log

def main():

    log.process(os.getpid())
    log.title("[{}] (PyTorch code for jointly optimizing NeRF and pose)".format(sys.argv[0]))

    opt_cmd = options.parse_arguments(sys.argv[1:])
    opt = options.set(opt_cmd=opt_cmd)
    options.save_options_file(opt)

    with torch.cuda.device(opt.device):

        model = importlib.import_module("model.{}".format(opt.model))
        log.model("************************************************** Running {} **************************************************".format(opt.model))
        
        m = model.Model(opt)
        m.load_dataset(opt)
        m.build_networks(opt)
        m.setup_optimizer(opt)
        m.restore_checkpoint(opt)
        m.setup_visualizer(opt)
        m.train(opt)
        log.model("************************************************** Done **************************************************")

if __name__=="__main__":
    main()
