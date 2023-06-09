# device-events-display

This service displays events for a device.  The events are specified by the device's mac address as well as the time interval.

## Bring up Development Environment Locally

To execute a local copy of the code that runs locally on host:
```sh
./mgr dev
```

This is useful when you're first developing the application.  A python  virtual environment is created if it doesn't exist.
When you edit a python file, uvicorn is restarted with your newly edited application.

This development strategy is faster than deploying the application inside a locally-running container, checking out if the
changes worked, re-building, re-deploying, etc.


## Build Container
```sh
./mgr build
```

The unit tests are run first.  If all of those pass, then the application's docker image is created.

## Push Container to Repository
```sh
./mgr push
```

## Deploy Container Locally
```sh
./mgr up
```

## Deploy Containers Into Kubernetes

Unfortunately, this hasn't been implemented yet.  We hope to create a separate git repository for this
such that the new repository contains helm charts and templates, and a values.yaml file...ArgoCD will deploy
if values.yaml changes. 
