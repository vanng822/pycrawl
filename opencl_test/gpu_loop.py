import pyopencl as cl
import numpy
import numpy.linalg as la
import time

a = numpy.random.rand(50000).astype(numpy.float32)
b = numpy.random.rand(50000).astype(numpy.float32)

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

mf = cl.mem_flags
a_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
b_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)
dest_buf = cl.Buffer(ctx, mf.WRITE_ONLY, b.nbytes)

prg = cl.Program(ctx, """
    __kernel void sum(__global const float *a,
    __global const float *b, __global float *c)
    {
        int gid = get_global_id(0);
	        c[gid] = a[gid] + b[gid];
    }
    __kernel void loop_sum(__global const float *a,
    __global const float *b, __global float *c)
    {
        int i = 0;
        while(i < 100000) {
            sum(a, b, c);
            i = i + 1;
        }
    }
    """).build()

prg.loop_sum(queue, a.shape, None, a_buf, b_buf, dest_buf)

a_plus_b = numpy.empty_like(a)
cl.enqueue_copy(queue, a_plus_b, dest_buf)

start = time.time()
t = la.norm(a_plus_b - (a+b)), la.norm(a_plus_b)
print(t)

print(time.time() - start)
