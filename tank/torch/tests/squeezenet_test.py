from shark.shark_inference import SharkInference
from shark.iree_utils import check_device_drivers
from tank.torch.tests.test_utils import get_vision_model, compare_tensors

import torch
import unittest
import numpy as np
import torchvision.models as models
import pytest

torch.manual_seed(0)

class SqueezenetModuleTester:

    def __init__(
        self,
        dynamic=False,
        device="cpu",
    ):
        self.dynamic = dynamic
        self.device = device

    def create_and_check_module(self):
        model, input, act_out = get_vision_model(models.squeezenet1_0(pretrained=True))
        shark_module = SharkInference(
                model,
                (input,),
                device=self.device,
                dynamic=self.dynamic,
        )
        shark_module.compile()
        results = shark_module.forward((input,))
        assert True == compare_tensors(act_out, results)

class SqueezenetModuleTest(unittest.TestCase):

    def setUp(self):
        self.module_tester = SqueezenetModuleTester(self)
        
    def test_module_static_cpu(self):
        self.module_tester.dynamic = False
        self.module_tester.device = "cpu"
        self.module_tester.create_and_check_module()
    
    def test_module_dynamic_cpu(self):
        self.module_tester.dynamic = True
        self.module_tester.device = "cpu"
        self.module_tester.create_and_check_module()
    
    @pytest.mark.skipif(check_device_drivers("gpu"), reason="nvidia-smi not found")
    def test_module_static_gpu(self):
        self.module_tester.dynamic = False
        self.module_tester.device = "gpu"
        self.module_tester.create_and_check_module()

    @pytest.mark.skipif(check_device_drivers("gpu"), reason="nvidia-smi not found")
    def test_module_dynamic_gpu(self):
        self.module_tester.dynamic = True
        self.module_tester.device = "gpu"
        self.module_tester.create_and_check_module()

    @pytest.mark.skipif(
            check_device_drivers("vulkan"),
            reason="vulkaninfo not found, install from https://github.com/KhronosGroup/MoltenVK/releases"
            )
    def test_module_static_vulkan(self):
        self.module_tester.dynamic = False
        self.module_tester.device = "vulkan"
        self.module_tester.create_and_check_module()

    @pytest.mark.skipif(
            check_device_drivers("vulkan"),
            reason="vulkaninfo not found, install from https://github.com/KhronosGroup/MoltenVK/releases"
            )
    def test_module_dynamic_vulkan(self):
        self.module_tester.dynamic = True
        self.module_tester.device = "vulkan"
        self.module_tester.create_and_check_module()


if __name__ == '__main__':
    unittest.main()
