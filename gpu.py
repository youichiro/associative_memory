from chainer import cuda

device = 1
cuda.get_device(device).use()
import cupy as np
np.cuda.set_allocator(np.cuda.MemoryPool().malloc)

