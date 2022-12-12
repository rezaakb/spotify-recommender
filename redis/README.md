# Redis database

We have provide a single-pod deployment that provides a Redis database and a service called `redis` so that worker nodes can use DNS names to locate the instance. The provided deployment uses [the image provided by the Redis developers](https://hub.docker.com/_/redis).

You don't need to create any database tables in advance -- that happens automatically when you start using the database; see instructions in `worker/README-worker.md`.

### *N.B.*

If you delete your redis pod, the database will also be deleted because we didn't provide a volume for the data. If you want to avoid that problem, you can create [a kubernetes Persistent Volume and Persistent Volume claim](https://cloud.google.com/kubernetes-engine/docs/concepts/persistent-volumes).

We're not using Redis because it's great, we're using it because it's easy, so if you don't want to have persistent data, don't bother. During development, it's actually useful to be able to delete all the data by killing the pod.